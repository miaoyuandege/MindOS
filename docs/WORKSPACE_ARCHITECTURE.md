# Workspace architecture

MindOS can begin inside one existing project and grow only when continuity needs grow. The layouts below are references, not installation requirements.

> **Reference layout ≠ mandatory filesystem layout.** Adapt MindOS to the conventions a project already has; do not restructure a healthy workspace just to match an example.

## Level 1 — One project / Minimal

The smallest useful setup keeps the execution Skill, protocol, and a few project-state files together:

```text
Project/
├─ .agents/
│  └─ skills/
│     └─ mindos/
│        └─ SKILL.md
├─ mindos-protocol/
│  ├─ MindOS.md
│  └─ templates/
├─ project-overview.md
├─ current-stage.md
├─ Current/
├─ Planning/
├─ Inbox/
└─ Handoffs/
```

The names may follow local language and repository conventions. What matters is that an AI can find the protocol, current truth, open plans, new inputs, and preserved handoffs without guessing.

This level needs no database, service, bot, Router, or background process. It is the recommended starting point for an existing Codex project.

## Level 2 — Multiple long-running projects / Shared workspace

When several projects need the same protocol, templates, or carefully distilled knowledge, a shared layer can reduce duplication:

```text
AI/
├─ MindOS-Global/
│  ├─ protocol/
│  ├─ shared-knowledge/
│  └─ templates/
├─ Project-A/
│  └─ MindOS-Project-A/
│     ├─ Current/
│     ├─ Planning/
│     ├─ Inbox/
│     └─ Handoffs/
├─ Project-B/
│  └─ MindOS-Project-B/
└─ optional-tools/
```

The shared layer owns only genuinely reusable material. Each project keeps its own current stage, decisions, tasks, evidence, and history. A shared file must not silently override a project's authority or mix private project state across boundaries.

## Level 3 — Optional integrations / Infrastructure

Teams with a demonstrated need can add integrations around the file-based core:

| Optional integration | Possible role |
| --- | --- |
| Read-only file bridge | Let an approved client inspect selected workspace roots |
| Router | Deliver a reviewed source to a known project Inbox |
| Observability | Read bounded Git, system, or task evidence |
| Remote entry | Submit a constrained request through an existing trusted channel |
| Runtime/task infrastructure | Track registered task state and execution evidence |

These are examples, not a v0.1 installation checklist. They are not bundled as ready-to-run infrastructure in this public pre-release, and more automation is not automatically better. Add one only after its permissions, failure behavior, and verification boundary are clear.

## Adoption ladder

1. **Start local:** install the project Skill and protocol, then point the overview at real Current, Planning, Inbox, and Handoffs locations.
2. **Prove continuity:** use a fresh chat to take over the project and complete one small, scoped, verified task.
3. **Share selectively:** add global templates or distilled knowledge only when multiple projects genuinely reuse them.
4. **Integrate deliberately:** add infrastructure only for a repeated problem that files and normal tools cannot solve cleanly.

For the concrete first step, use the [Quick Start](QUICK_START.md). To see the collaboration loop in context, continue to the [walkthrough](WALKTHROUGH.md).
