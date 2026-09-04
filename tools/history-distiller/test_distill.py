# Synthetic fixtures only; no real sessions, model claims or project identities.
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import distill as d


def row(kind, payload, when="2026-09-04T01:00:00Z"):
    return {"type":kind,"timestamp":when,"payload":payload}


def meta(sid, parent=None, depth=0, when="2026-09-04T01:00:00Z", name=None):
    a={"id":sid,"timestamp":when,"cwd":"projects/Example","cli_version":"fixture-client","source":"vscode"}
    if parent:
        a.update(parent_thread_id=parent,agent_path=name or "/root/test",source={"subagent":{"thread_spawn":{"parent_thread_id":parent,"depth":depth}}})
    return row("session_meta",a,when)


def ctx(model="gpt-example-root", effort="max", when="2026-09-04T01:00:00Z"):
    return row("turn_context",{"model":model,"effort":effort,"multi_agent_version":"v2"},when)


class DistillerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name)
        self.sessions=self.base/"sessions"; self.sessions.mkdir()
        self.archived=self.base/"archived"; self.archived.mkdir()
        self.start=datetime(2026,8,27,16,tzinfo=timezone.utc)
        self.end=datetime(2026,9,4,16,tzinfo=timezone.utc)

    def write(self, name, rows, archived=False):
        p=(self.archived if archived else self.sessions)/name
        p.write_text("".join(json.dumps(x)+"\n" if isinstance(x,dict) else x for x in rows),encoding="utf-8")
        return p

    def parse(self,p):
        desc={"path":str(p),"size":p.stat().st_size,"sha256":d.hash_prefix(p,p.stat().st_size)}
        return d.parse_file(p,desc,self.start,self.end)

    def args(self,out,manifest=None):
        return argparse.Namespace(sessions_root=str(self.sessions),archived_root=str(self.archived),output=str(out),
                                  from_date="2026-08-28",to_date="2026-09-04",project=None,manifest=str(manifest) if manifest else None)

    def test_topology_requested_vs_effective_and_unknown(self):
        call=row("response_item",{"type":"function_call","name":"spawn_agent","call_id":"call_1","arguments":json.dumps({"task_name":"test","model":"gpt-example-child","reasoning_effort":"high","fork_turns":"none","message":"SECRET_USER_PROMPT"})})
        output=row("response_item",{"type":"function_call_output","call_id":"call_1","output":json.dumps({"task_name":"/root/test"})},"2026-09-04T01:00:02Z")
        root=self.parse(self.write("root.jsonl",[meta("root"),ctx(),call,output]))
        child=self.parse(self.write("child.jsonl",[meta("child","root",1,"2026-09-04T01:00:01Z"),ctx(when="2026-09-04T01:00:01Z")]))
        grand=self.parse(self.write("grand.jsonl",[meta("grand","child",2,name="/root/test/grand"),ctx()]))
        d.build_topology([root,child,grand])
        self.assertEqual(grand["topology_depth"],2)
        self.assertEqual(root["fan_out"],1)
        self.assertEqual(child["receipt"]["routing_result"],"MISMATCH")
        self.assertEqual(child["receipt"]["effective"]["fork_mode"],d.UNKNOWN)
        self.assertEqual(grand["receipt"]["routing_result"],d.UNKNOWN)
        self.assertNotIn("SECRET_USER_PROMPT",d.stable_json([root,child]))

    def test_latest_counters_first_footprint_not_sum(self):
        def token(n):return row("event_msg",{"type":"token_count","info":{"total_token_usage":{"input_tokens":n,"cached_input_tokens":n//2,"output_tokens":20,"reasoning_output_tokens":10},"last_token_usage":{"input_tokens":100}},"rate_limits":{"primary":{"used_percent":12,"window_minutes":300},"credits":{"balance":"PRIVATE_BALANCE"}}})
        s=self.parse(self.write("token.jsonl",[meta("root"),ctx(),token(200),token(800),row("event_msg",{"type":"task_complete","last_agent_message":"PRIVATE_FINAL"})]))
        self.assertEqual(s["first_token_snapshot_in_window"]["last_request"]["input_tokens"],100)
        self.assertEqual(s["latest_token_snapshot"]["cumulative"]["input_tokens"],800)
        self.assertEqual(s["latest_token_snapshot"]["cumulative"]["uncached_input_tokens"],400)
        self.assertEqual(s["final_status"],"task_complete")
        self.assertNotIn("PRIVATE",d.stable_json(s))

    def test_malformed_missing_inherited_and_opaque_reasoning(self):
        s=self.parse(self.write("missing.jsonl",[meta("child","root",1),ctx(when="2026-09-03T01:00:00Z"),"{broken\n",row("turn_context",{}),row("response_item",{"type":"reasoning","encrypted_content":"SECRET_ENCRYPTED"}),"partial"]))
        self.assertEqual(s["effective_model"],d.UNKNOWN)
        self.assertEqual(s["parse_quality"]["malformed_lines"],1)
        self.assertEqual(s["parse_quality"]["partial_tail_lines"],1)
        self.assertEqual(s["parse_quality"]["ignored_pre_metadata_or_inherited_records"],1)
        self.assertNotIn("SECRET_ENCRYPTED",d.stable_json(s))

    def test_guardian_not_spawn_and_mixed_effort_bins(self):
        g=meta("guard","root")
        g["payload"]["source"]={"subagent":{"other":"guardian"}}
        guardian=self.parse(self.write("guard.jsonl",[g,ctx("codex-auto-review","low")]))
        root=self.parse(self.write("root.jsonl",[meta("root"),ctx(effort="high"),ctx(effort="max")]))
        d.build_topology([root,guardian])
        summary=d.summarize([root,guardian])
        self.assertEqual(root["fan_out"],0)
        self.assertEqual(summary["by_root_effort"]["low"]["root_sessions_observed"],0)
        self.assertEqual(summary["by_root_effort"]["high"]["root_sessions_observed"],1)
        self.assertEqual(summary["by_root_effort"]["max"]["root_sessions_observed"],1)

    def test_determinism_prefix_replay_no_mutation_and_archive(self):
        p=self.write("root.jsonl",[meta("root"),ctx()])
        q=self.write("child.jsonl",[meta("child","root",1),ctx()],True)
        before={f:f.read_bytes() for f in (p,q)}
        one=self.base/"one"; two=self.base/"two"
        d.run(self.args(one))
        # Appending a concurrent later event does not change the captured input prefix.
        with p.open("a",encoding="utf-8") as f:f.write(json.dumps(ctx(effort="high"))+"\n")
        after_append=p.read_bytes()
        d.run(self.args(two,one/"manifest.json"))
        for name in ("observations.json","observations.md","manifest.json"):
            self.assertEqual((one/name).read_bytes(),(two/name).read_bytes())
        self.assertEqual(p.read_bytes(),after_append)
        self.assertEqual(q.read_bytes(),before[q])

    def test_output_input_overlap_fail_closed(self):
        self.write("root.jsonl",[meta("root"),ctx()])
        for path in (self.sessions/"out",self.base,self.base/".codex"/"out",self.base/".agents"/"out"):
            with self.assertRaises(ValueError):d.run(self.args(path))

    def test_changed_prefix_and_manifest_escape_fail_closed(self):
        p=self.write("root.jsonl",[meta("root"),ctx()])
        out=self.base/"one"; d.run(self.args(out))
        p.write_text("changed\n",encoding="utf-8")
        with self.assertRaises(ValueError):d.run(self.args(self.base/"two",out/"manifest.json"))
        manifest=json.loads((out/"manifest.json").read_text())
        manifest["inputs"][0]["path"]=str(self.base/"outside.jsonl")
        (self.base/"outside.jsonl").write_text("private",encoding="utf-8")
        (out/"escape.json").write_text(json.dumps(manifest),encoding="utf-8")
        with self.assertRaises(ValueError):d.run(self.args(self.base/"three",out/"escape.json"))

    def test_empty_and_no_low_medium_claim(self):
        summary=d.summarize([])
        for level in d.EFFORTS:
            self.assertEqual(summary["by_root_effort"][level]["evidence_status"],"INSUFFICIENT_EVIDENCE")

    def test_project_filter_and_date_boundary(self):
        self.write("keep.jsonl",[meta("keep"),ctx()])
        other=meta("other");other["payload"]["cwd"]="projects/Other"
        self.write("other.jsonl",[other,ctx()])
        self.write("after.jsonl",[meta("after",when="2026-09-04T16:00:00Z"),ctx(when="2026-09-04T16:00:00Z")])
        args=self.args(self.base/"filtered");args.project="example"
        d.run(args)
        data=json.loads((self.base/"filtered/observations.json").read_text())
        self.assertEqual([s["session_id"] for s in data["sessions"]],["keep"])

    def test_retimestamped_parent_history_not_child_receipt(self):
        inherited=ctx(effort="max")
        inherited["payload"]["turn_id"]="parent-turn"
        actual=ctx(effort="ultra")
        actual["payload"]["turn_id"]="child-turn"
        p=self.write("child.jsonl",[meta("child","root",1),meta("root"),inherited,
            row("event_msg",{"type":"task_started","turn_id":"parent-turn"}),
            row("event_msg",{"type":"token_count","info":{"total_token_usage":{"input_tokens":999999}}}),
            row("event_msg",{"type":"task_started","turn_id":"child-turn"}),actual])
        desc={"path":str(p),"size":p.stat().st_size,"sha256":d.hash_prefix(p,p.stat().st_size)}
        child=d.parse_file(p,desc,self.start,self.end,{"parent-turn"})
        self.assertEqual([c["effort"] for c in child["contexts"]],["ultra"])
        self.assertEqual(child["latest_token_snapshot"],d.UNKNOWN)
        self.assertEqual(child["parse_quality"]["inherited_identity_records"],3)


if __name__=="__main__":unittest.main()
