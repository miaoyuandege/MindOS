"""Offline allowlisted projections of Codex JSONL. No model/network/shell calls."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re

UNKNOWN = "UNKNOWN"
EFFORTS = ("low", "medium", "high", "xhigh", "ultra", "max")
TOKENS = ("input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens", "total_tokens")
MAX_LINE = 8 * 1024 * 1024
TASK_RE = re.compile(r"\b(?:MINDOS-[A-Z0-9][A-Z0-9.-]{5,120}|20\d{9})\b")
SECRET_RE = re.compile(r"(?i)(?:sk-|bearer|api[_-]?key|auth[_-]?token|secret|encrypted)")


def stable_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def stamp(value):
    try:
        t = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return t.astimezone(timezone.utc) if t.tzinfo else None
    except (AttributeError, ValueError, TypeError):
        return None


def label(value, pattern=r"[\w./ :\\-]{1,240}"):
    if not isinstance(value, str) or SECRET_RE.search(value) or not re.fullmatch(pattern, value):
        return UNKNOWN
    return value


def model(value):
    return label(value, r"(?:gpt-[a-zA-Z0-9_.-]+|codex-[a-zA-Z0-9_.-]+)")


def effort(value):
    return value if value in EFFORTS else UNKNOWN


def fork(value):
    if value in ("all", "none"):
        return value
    if isinstance(value, (str, int)) and str(value).isdigit() and 1 <= int(value) <= 10000:
        return str(value)
    return UNKNOWN


def token_projection(value):
    value = value if isinstance(value, dict) else {}
    result = {k: v for k in TOKENS if type(v := value.get(k)) is int and v >= 0}
    inp, cached = result.get("input_tokens"), result.get("cached_input_tokens")
    result["uncached_input_tokens"] = inp - cached if inp is not None and cached is not None and cached <= inp else UNKNOWN
    result["cached_ratio"] = round(cached / inp, 6) if inp and cached is not None and cached <= inp else UNKNOWN
    return result


def rate_projection(value):
    result = {}
    if isinstance(value, dict):
        for key in ("primary", "secondary"):
            window = value.get(key)
            if isinstance(window, dict):
                result[key] = {k: v for k in ("used_percent", "window_minutes", "resets_at")
                               if type(v := window.get(k)) in (int, float)}
    return result or UNKNOWN


def role_of(path):
    # A conservative *label hypothesis*, never evidence of usefulness/duplication.
    words = path.lower().replace("-", "_") if isinstance(path, str) else ""
    rules = [("re_audit", "re-audit"), ("reaudit", "re-audit"), ("standards", "standards-review"),
             ("spec_review", "spec-review"), ("review", "review"), ("verify", "verification"),
             ("verification", "verification"), ("test", "test"), ("research", "research / repo-map"),
             ("repo_map", "research / repo-map"), ("client", "client"), ("server", "server"),
             ("host", "host / integration"), ("integrat", "host / integration"), ("implement", "implementation"),
             ("docs", "docs"), ("runtime_rescan", "runtime-rescan"), ("knowledge", "knowledge-governance")]
    return next((role for word, role in rules if word in words), "unknown")


def hash_prefix(path, size):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        remaining = size
        while remaining:
            data = stream.read(min(1024 * 1024, remaining))
            if not data:
                raise ValueError("INPUT_TRUNCATED")
            digest.update(data)
            remaining -= len(data)
    return digest.hexdigest()


def records(path, size, quality):
    """Bounded line reads; oversized lines never produce output or partial records."""
    with path.open("rb") as stream:
        remaining, number = size, 0
        while remaining:
            raw = stream.readline(min(MAX_LINE + 1, remaining))
            if not raw:
                raise ValueError("INPUT_TRUNCATED")
            remaining -= len(raw)
            number += 1
            if len(raw) > MAX_LINE:
                while not raw.endswith(b"\n") and remaining:
                    raw = stream.readline(min(MAX_LINE, remaining))
                    remaining -= len(raw)
                quality["oversized_lines"] += 1
                continue
            if not raw.endswith(b"\n"):
                quality["partial_tail_lines"] += 1
                continue
            try:
                row = json.loads(raw.decode("utf-8-sig"))
            except (ValueError, UnicodeError, RecursionError):
                quality["malformed_lines"] += 1
                continue
            if isinstance(row, dict):
                yield number, row


def scan_identity(path, descriptor):
    result = {"session_id": UNKNOWN, "parent": UNKNOWN, "fork_parent": UNKNOWN, "turn_ids": set()}
    for _,row in records(path,descriptor["size"],Counter()):
        a=row.get("payload",{})
        if not isinstance(a,dict):
            continue
        if row.get("type")=="session_meta" and result["session_id"]==UNKNOWN:
            source=a.get("source",{})
            sub=source.get("subagent",{}) if isinstance(source,dict) else {}
            spawned=sub.get("thread_spawn",{}) if isinstance(sub,dict) else {}
            spawned=spawned if isinstance(spawned,dict) else {}
            result.update(session_id=label(a.get("id") or a.get("session_id")),
                          parent=label(a.get("parent_thread_id") or spawned.get("parent_thread_id")),
                          fork_parent=label(a.get("forked_from_id")))
        if row.get("type")=="turn_context" or (row.get("type")=="event_msg" and a.get("type")=="task_started"):
            if isinstance(a.get("turn_id"),str):
                result["turn_ids"].add(a["turn_id"])
    return result


def parse_file(path, descriptor, start, end, inherited_turn_ids=frozenset()):
    quality = Counter()
    session = None
    latest_context = {"model": UNKNOWN, "effort": UNKNOWN, "multi_agent_version": UNKNOWN}
    contexts, spawns, pending = [], [], {}
    first_token, latest_token, latest_rate, peak_token = None, None, None, None
    counter_decreases = 0
    task_ids = set()
    active_turn, last_lifecycle = False, UNKNOWN
    last_event = None
    window_events = 0
    meta_time = None
    inherited_segment = False
    for line, row in records(path, descriptor["size"], quality):
        kind, payload = row.get("type"), row.get("payload")
        if not isinstance(payload, dict):
            continue
        now = stamp(row.get("timestamp"))
        if kind == "session_meta":
            if session is not None:
                quality["additional_session_meta"] += 1
                inherited_segment = True
                continue
            source = payload.get("source", {})
            sub = source.get("subagent", {}) if isinstance(source, dict) else {}
            spawned = sub.get("thread_spawn", {}) if isinstance(sub, dict) else {}
            if not isinstance(spawned, dict):
                spawned = {}
            parent = label(payload.get("parent_thread_id") or spawned.get("parent_thread_id"))
            session_kind = "guardian" if isinstance(sub, dict) and sub.get("other") == "guardian" else (
                "child" if parent != UNKNOWN or spawned else "root")
            meta_time = stamp(payload.get("timestamp")) or now
            session = {
                "session_id": label(payload.get("id") or payload.get("session_id")),
                "parent_thread_id": parent, "kind": session_kind,
                "agent_path": label(payload.get("agent_path") or spawned.get("agent_path")),
                "agent_nickname": label(payload.get("agent_nickname") or spawned.get("agent_nickname")),
                "depth_reported": spawned.get("depth") if type(spawned.get("depth")) is int else UNKNOWN,
                "cwd": label(payload.get("cwd")), "cli_version": label(payload.get("cli_version")),
                "originator": label(payload.get("originator")),
                "start_time": meta_time.isoformat() if meta_time else UNKNOWN,
                "forked_from_id": label(payload.get("forked_from_id")),
                "effective_fork_mode": fork(payload.get("fork_turns")),
                "rollout_path": str(path), "metadata_line": line,
            }
            continue
        if session is None or now is None or meta_time is None or now < meta_time:
            quality["ignored_pre_metadata_or_inherited_records"] += 1
            continue
        event = payload.get("type")
        if kind == "turn_context" or (kind == "event_msg" and event == "task_started"):
            tid=payload.get("turn_id")
            if tid:
                inherited_segment = tid in inherited_turn_ids
        if inherited_segment:
            quality["inherited_identity_records"] += 1
            continue
        if now >= end:
            continue
        # Old context needed for a resumed root; metrics only count events in the window.
        if kind == "turn_context":
            latest_context = {"model": model(payload.get("model")), "effort": effort(payload.get("effort")),
                              "multi_agent_version": label(payload.get("multi_agent_version"))}
            if now >= start:
                ctx = {**latest_context, "time": now.isoformat(), "line": line, "turn_id": label(payload.get("turn_id"))}
                contexts.append(ctx)
        if now < start:
            continue
        window_events += 1
        last_event = max(last_event, now) if last_event else now
        if kind == "event_msg":
            if event == "token_count":
                info = payload.get("info") or {}
                if isinstance(info, dict) and isinstance(info.get("total_token_usage"), dict):
                    tok = {"time": now.isoformat(), "line": line,
                           "cumulative": token_projection(info["total_token_usage"]),
                           "last_request": token_projection(info.get("last_token_usage")),
                           "model_context_window": info.get("model_context_window") if type(info.get("model_context_window")) is int else UNKNOWN}
                    if first_token is None:
                        first_token = tok
                    if latest_token and tok["cumulative"].get("input_tokens",0) < latest_token["cumulative"].get("input_tokens",0):
                        counter_decreases += 1
                    if peak_token is None or tok["last_request"].get("input_tokens",0) > peak_token["last_request"].get("input_tokens",0):
                        peak_token = tok
                    latest_token = tok
                latest_rate = {"time": now.isoformat(), "windows": rate_projection(payload.get("rate_limits"))}
            elif event in ("task_started", "task_complete", "turn_aborted"):
                active_turn = event == "task_started"
                last_lifecycle = event
            elif event == "user_message":
                # Whitelisted IDs only, not user message text.
                text = payload.get("message", "")
                if isinstance(text, str):
                    task_ids.update(TASK_RE.findall(text))
        if kind != "response_item":
            continue
        if event == "message" and payload.get("role") == "user":
            for part in payload.get("content",[]) if isinstance(payload.get("content"),list) else []:
                if isinstance(part,dict) and isinstance(part.get("text"),str):
                    task_ids.update(t for t in TASK_RE.findall(part["text"]) if not SECRET_RE.search(t))
        if event == "function_call" and payload.get("name", "").split(".")[-1] == "spawn_agent":
            try:
                arguments = json.loads(payload.get("arguments", "{}"))
            except (ValueError, TypeError):
                arguments = {}
            if not isinstance(arguments, dict):
                arguments = {}
            requested = {"model": model(arguments.get("model")), "effort": effort(arguments.get("reasoning_effort")),
                         "fork_turns": fork(arguments.get("fork_turns")), "role": role_of(arguments.get("task_name"))}
            message = arguments.get("message")
            call = {"line": line, "time": now.isoformat(), "call_id": label(payload.get("call_id")),
                    "task_name": label(arguments.get("task_name")), "requested": requested,
                    "parent_context": dict(latest_context), "child_session_id": UNKNOWN,
                    "returned_agent_path": UNKNOWN,
                    "scope_sha256": hashlib.sha256(message.encode()).hexdigest() if isinstance(message, str) else UNKNOWN,
                    "task_ids": sorted(set(TASK_RE.findall(message))) if isinstance(message, str) else [],
                    "output_line": UNKNOWN, "output_time": UNKNOWN, "failure_category": UNKNOWN}
            spawns.append(call)
            pending[call["call_id"]] = call
        elif event == "function_call_output" and payload.get("call_id") in pending:
            call = pending[payload["call_id"]]
            raw_output = payload.get("output", "")
            if isinstance(raw_output,str):
                if re.search(r"(?i)(?:limit.{0,30}reached|agent.{0,30}limit|maximum.{0,30}agent)", raw_output):
                    call["failure_category"] = "SPAWN_LIMIT"
                elif re.search(r"(?i)already exists", raw_output):
                    call["failure_category"] = "NAME_ALREADY_EXISTS"
            try:
                output = json.loads(payload.get("output", "{}"))
            except (ValueError, TypeError):
                output = {}
            if isinstance(output, dict):
                call["child_session_id"] = label(output.get("agent_id") or output.get("thread_id"))
                call["returned_agent_path"] = label(output.get("task_name"))
                call["output_line"], call["output_time"] = line, now.isoformat()
    if session is None or not window_events:
        return None
    session.update({"last_observed_time": last_event.isoformat(), "observed_span_seconds": round((last_event-meta_time).total_seconds(), 3),
                    "final_status": "RUNNING_AT_LAST_EVENT" if active_turn else last_lifecycle,
                    "formal_completion": "NOT_INFERRED", "effective_model": latest_context["model"],
                    "effective_effort": latest_context["effort"], "multi_agent_version": latest_context["multi_agent_version"],
                    "contexts": contexts, "spawns": spawns, "first_token_snapshot_in_window": first_token or UNKNOWN,
                    "peak_request_snapshot": peak_token or UNKNOWN, "cumulative_counter_decreases": counter_decreases,
                    "latest_token_snapshot": latest_token or UNKNOWN, "latest_rate_limit_snapshot": latest_rate or UNKNOWN,
                    "task_ids": sorted(task_ids), "parse_quality": dict(quality),
                    "role_candidate": role_of(session["agent_path"]), "role_confidence": "label_only",
                    "input": descriptor})
    return session


def build_topology(sessions):
    by_id = {s["session_id"]: s for s in sessions if s["session_id"] != UNKNOWN}
    for s in sessions:
        depth, at, seen = 0, s, set()
        while at["kind"] == "child" and at["parent_thread_id"] in by_id and at["session_id"] not in seen:
            seen.add(at["session_id"])
            at = by_id[at["parent_thread_id"]]
            depth += 1
        s["topology_depth"] = depth if at["kind"] == "root" else UNKNOWN
        s["root_session_id"] = at["session_id"] if at["kind"] == "root" else UNKNOWN
        s["child_session_ids"] = sorted(c["session_id"] for c in sessions if c["kind"] == "child" and c["parent_thread_id"] == s["session_id"])
        s["fan_out"] = len(s["child_session_ids"])
        s["spawn_count"] = len(s["spawns"])
        s["receipt"] = {"requested": {k: UNKNOWN for k in ("model", "effort", "role", "fork_turns")},
                         "effective": {"model": s["effective_model"], "effort": s["effective_effort"],
                                       "parent": s["parent_thread_id"], "depth": s["topology_depth"], "fork_mode": s["effective_fork_mode"]},
                         "routing_result": UNKNOWN, "link_evidence": UNKNOWN}
    for parent in sessions:
        for call in parent["spawns"]:
            candidates = [s for s in sessions if s["kind"] == "child" and s["parent_thread_id"] == parent["session_id"] and (
                (call["child_session_id"] != UNKNOWN and s["session_id"] == call["child_session_id"]) or (
                    call["returned_agent_path"] != UNKNOWN and s["agent_path"] == call["returned_agent_path"] and
                    stamp(call["time"]) <= stamp(s["start_time"]) <= (stamp(call["output_time"]) or stamp(call["time"])) + timedelta(seconds=2)))]
            if len(candidates) != 1:
                call["link_result"] = "UNRESOLVED" if not candidates else "AMBIGUOUS"
                continue
            child = candidates[0]
            call["child_session_id"], call["link_result"] = child["session_id"], "LINKED"
            # Earliest child-owned context is the effective spawn receipt, not final resumed context.
            ctx = child["contexts"][0] if child["contexts"] else {}
            effective = {"model": ctx.get("model", UNKNOWN), "effort": ctx.get("effort", UNKNOWN),
                         "parent": child["parent_thread_id"], "depth": child["topology_depth"], "fork_mode": child["effective_fork_mode"]}
            pairs = [(call["requested"][k], effective[k]) for k in ("model", "effort")]
            routing = "MISMATCH" if any(a != UNKNOWN and b != UNKNOWN and a != b for a,b in pairs) else (
                "MATCH" if all(a != UNKNOWN and b != UNKNOWN for a,b in pairs) else UNKNOWN)
            child["receipt"] = {"requested": call["requested"], "effective": effective, "routing_result": routing,
                                "link_evidence": {"parent_session_id": parent["session_id"], "parent_rollout_path": parent["rollout_path"],
                                                  "call_line": call["line"], "output_line": call["output_line"],
                                                  "child_metadata_line": child["metadata_line"], "method": "explicit parent ID + returned ID/path + unique timestamp window"}}


def summarize(sessions):
    roots = [s for s in sessions if s["kind"] == "root"]
    bins = {}
    for level in EFFORTS:
        exposed = [s for s in roots if any(c["effort"] == level for c in s["contexts"])]
        calls = [(s,c) for s in roots for c in s["spawns"] if c["parent_context"]["effort"] == level]
        spawned_ids = {c["child_session_id"] for _,c in calls if c["link_result"] == "LINKED"}
        children = [s for s in sessions if s["session_id"] in spawned_ids]
        descendants = [s for s in sessions if s["root_session_id"] in {r["session_id"] for r,c in calls} and s["kind"]=="child"]
        bins[level] = {"root_sessions_observed": len(exposed), "root_sessions_with_spawn_calls": len({s["session_id"] for s,c in calls}),
                       "spawn_calls": len(calls), "linked_direct_children": len(children),
                       "child_models": dict(sorted(Counter(s["receipt"]["effective"]["model"] for s in children).items())),
                       "common_role_candidates": dict(sorted(Counter(s["role_candidate"] for s in children).items())),
                       "root_session_ids": sorted(s["session_id"] for s in exposed),
                       "max_descendant_depth_in_exposed_roots": max((s["topology_depth"] for s in descendants if type(s["topology_depth"]) is int),default=0),
                       "version_cohorts": dict(sorted(Counter(s["cli_version"] for s in exposed).items())),
                       "project_cohorts": dict(sorted(Counter(s["cwd"] for s in exposed).items())),
                       "evidence_status": "OBSERVED_CORRELATION_ONLY" if len(exposed) >= 3 else "INSUFFICIENT_EVIDENCE"}
    overlaps = []
    review_roles = {"review", "spec-review", "standards-review", "re-audit", "verification"}
    for root in sessions:
        children = [s for s in sessions if s["kind"] == "child" and s["parent_thread_id"] == root["session_id"] and s["role_candidate"] in review_roles]
        for i,a in enumerate(children):
            for b in children[i+1:]:
                if max(stamp(a["start_time"]),stamp(b["start_time"])) <= min(stamp(a["last_observed_time"]),stamp(b["last_observed_time"])):
                    overlaps.append({"parent_session_id":root["session_id"], "sessions":[a["session_id"],b["session_id"]],
                                     "roles":[a["role_candidate"],b["role_candidate"]], "duplicate_work": "NOT_ESTABLISHED", "unique_findings": UNKNOWN})
    return {"sessions":len(sessions), "kind_counts":dict(sorted(Counter(s["kind"] for s in sessions).items())),
            "by_root_effort": bins, "max_topology_depth":max((s["topology_depth"] for s in sessions if type(s["topology_depth"]) is int), default=0),
            "max_fan_out":max((s["fan_out"] for s in sessions),default=0), "child_spawning_sessions":sum(s["kind"]=="child" and s["spawn_count"]>0 for s in sessions),
            "spawn_failure_categories":dict(sorted(Counter(c["failure_category"] for s in sessions for c in s["spawns"] if c["failure_category"]!=UNKNOWN).items())),
            "review_overlap_candidates":overlaps}


def markdown(data):
    s = data["summary"]
    lines = ["# Codex History Distillation", "", "Offline metadata only. Historical observations, not billing, causal effect, or Acceptance.", "",
             f"Window: {data['window']['from']} through {data['window']['to']} ({data['window']['timezone']}).", "",
             f"Sessions: {s['sessions']}; kinds: {json.dumps(s['kind_counts'])}; max depth: {s['max_topology_depth']}; max fan-out: {s['max_fan_out']}.", "",
             "## Root effort exposure (a changing root can occur in multiple rows)", "",
             "| Effort | Roots exposed | Roots with spawn calls | Calls | Linked children | Evidence |", "| --- | ---: | ---: | ---: | ---: | --- |"]
    for level,b in s["by_root_effort"].items():
        lines.append(f"| {level} | {b['root_sessions_observed']} | {b['root_sessions_with_spawn_calls']} | {b['spawn_calls']} | {b['linked_direct_children']} | {b['evidence_status']} |")
    lines += ["", "## Boundaries", "", "- Guardians are not intentional native child spawns. Child linkage uses explicit parent identity, never nickname.",
              "- Latest cumulative tokens are session counters, not an additive invoice; reasoning is a subset of output. Cached input is not free quota.",
              "- First snapshot in the date window is not necessarily the first request ever. Requested fork all is not an effective fork receipt.",
              "- Rate limits are shared-window snapshots: never summed across sessions.",
              "- Effort, project/task complexity, version, prompts, instructions and duration are confounders. Zero observed is not cannot spawn.",
              "- Review overlaps are candidates; duplicate work or lack of unique findings is not established.",
              "- Active logs are captured at fixed prefix sizes; append-only concurrent activity is not tool mutation.", "", "## Session index", "",
              "| ID | Kind | Parent | Depth | Effective model/effort (last observed) | Role candidate |", "| --- | --- | --- | --- | --- | --- |"]
    for a in data["sessions"]:
        lines.append(f"| {a['session_id']} | {a['kind']} | {a['parent_thread_id']} | {a['topology_depth']} | {a['effective_model']}/{a['effective_effort']} | {a['role_candidate']} |")
    return "\n".join(lines)+"\n"


def inside(path, root):
    return path == root or root in path.parents


def run(args):
    roots = [Path(args.sessions_root).resolve(strict=True), Path(args.archived_root).resolve(strict=True)]
    out = Path(args.output).resolve()
    if any(inside(out,r) or inside(r,out) for r in roots) or any(p.lower() in {".codex", ".agents"} for p in out.parts):
        raise ValueError("OUTPUT_OVERLAPS_PROTECTED_INPUT")
    if out.exists():
        raise ValueError("OUTPUT_EXISTS_USE_NEW_DIRECTORY")
    tz = timezone(timedelta(hours=8))
    start = datetime.fromisoformat(args.from_date).replace(tzinfo=tz).astimezone(timezone.utc)
    end = (datetime.fromisoformat(args.to_date)+timedelta(days=1)).replace(tzinfo=tz).astimezone(timezone.utc)
    if start >= end:
        raise ValueError("INVALID_WINDOW")
    if args.manifest:
        manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        if manifest["window"] != {"from":args.from_date,"to":args.to_date,"timezone":"UTC+08:00"}:
            raise ValueError("MANIFEST_WINDOW_MISMATCH")
        descriptors = manifest["inputs"]
    else:
        descriptors = []
        seen = set()
        for root in roots:
            for p in sorted(root.rglob("*.jsonl")):
                resolved = p.resolve(strict=True)
                if not inside(resolved,root) or resolved in seen:
                    continue
                seen.add(resolved)
                st = resolved.stat()
                # Include older resumed roots, not just files created within the window.
                if st.st_mtime < start.timestamp():
                    continue
                descriptors.append({"path":str(resolved),"size":st.st_size,"sha256":hash_prefix(resolved,st.st_size)})
    identity_rows = {}
    for desc in sorted(descriptors,key=lambda x:x["path"]):
        p = Path(desc["path"]).resolve(strict=True)
        if not any(inside(p,r) for r in roots) or p.suffix != ".jsonl" or type(desc["size"]) is not int or desc["size"]<0:
            raise ValueError("MANIFEST_INPUT_OUTSIDE_ROOTS")
        if hash_prefix(p,desc["size"]) != desc["sha256"]:
            raise ValueError("INPUT_PREFIX_CHANGED")
        identity_rows[desc["path"]]=scan_identity(p,desc)
    identities={i["session_id"]:i for i in identity_rows.values()}
    sessions = []
    for desc in sorted(descriptors,key=lambda x:x["path"]):
        p=Path(desc["path"])
        identity=identity_rows[desc["path"]]
        ancestor_ids=set()
        todo=[identity["parent"],identity["fork_parent"]]
        seen=set()
        while todo:
            sid=todo.pop()
            if sid in seen or sid==UNKNOWN or sid==identity["session_id"]:
                continue
            seen.add(sid)
            if sid in identities:
                ancestor=identities[sid]
                ancestor_ids.update(ancestor["turn_ids"])
                todo += [ancestor["parent"],ancestor["fork_parent"]]
        session = parse_file(p,desc,start,end,ancestor_ids)
        if hash_prefix(p,desc["size"]) != desc["sha256"]:
            raise ValueError("INPUT_CHANGED_DURING_PARSE")
        if session and (not args.project or args.project.casefold() in session["cwd"].casefold()):
            sessions.append(session)
    ids = [s["session_id"] for s in sessions]
    if len(ids) != len(set(ids)):
        raise ValueError("DUPLICATE_SESSION_ID_REQUIRES_RECONCILIATION")
    sessions.sort(key=lambda x:(x["start_time"],x["session_id"]))
    build_topology(sessions)
    window = {"from":args.from_date,"to":args.to_date,"timezone":"UTC+08:00"}
    data = {"schema":"codex-history-distiller@0.1", "window":window,"project_filter":args.project or None,
            "sessions":sessions,"summary":summarize(sessions),"input_integrity":"fixed prefixes verified before and after parsing"}
    out.mkdir(parents=True)
    for name,body in (("observations.json",stable_json(data)),("observations.md",markdown(data)),
                      ("manifest.json",stable_json({"window":window,"inputs":sorted(descriptors,key=lambda x:x["path"])}))):
        with (out/name).open("x",encoding="utf-8",newline="\n") as stream:
            stream.write(body)
    print(json.dumps({"sessions":len(sessions),"output":str(out),"input_prefixes":len(descriptors)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sessions-root", required=True)
    parser.add_argument("--archived-root", required=True)
    parser.add_argument("--from-date", required=True)
    parser.add_argument("--to-date", required=True)
    parser.add_argument("--project", "--cwd", dest="project")
    parser.add_argument("--output", required=True)
    parser.add_argument("--manifest", help="Replay identical immutable input prefixes, including active logs")
    try:
        run(parser.parse_args())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        # Do not print raw file data, exception payloads, or secret-bearing arguments.
        print(json.dumps({"error":type(exc).__name__,"detail":"Input/option check failed; no session writes. Inspect documented preconditions."}))
        raise SystemExit(2)
