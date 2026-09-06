# Public pretest file disposition

54 exact candidate files; PUBLIC PRE-RELEASE TEST, MIT LICENSED, NOT v0.1 FINAL, EXTERNAL FIRST-USE TESTING. RELEASE below means allowlisted for the explicitly authorized public test, not a final release; licensing is governed by [LICENSE](../LICENSE). No private source, completed real report or account data is included.

| File | Disposition | Purpose |
| --- | --- | --- |
| .gitignore | RELEASE | Reviewed public source, documentation or verification |
| CONTRIBUTING.md | RELEASE | Reviewed public source, documentation or verification |
| LICENSE | RELEASE | Standard MIT License; Copyright (c) 2026 miaoyuandege |
| README.md | RELEASE | Reviewed public source, documentation or verification |
| SECURITY.md | RELEASE | Reviewed public source, documentation or verification |
| START_HERE.md | RELEASE | Reviewed public source, documentation or verification |
| assets/mindos-hero.svg | RELEASE | Original font-free README hero; fixed light surface for light/dark hosts |
| assets/mindos-mark.svg | RELEASE | Original compact MindOS mark |
| assets/mindos-workflow.svg | RELEASE | Original four-step collaboration-loop visual |
| assets/social-preview.png | RELEASE | Deterministic 1280 x 640 social-preview render |
| assets/social-preview.svg | RELEASE | Original editable source for the social preview |
| chatgpt/custom-instructions/generic.md | RELEASE | Reviewed public source, documentation or verification |
| codex/profiles/guardrails.md | RELEASE | Reviewed public source, documentation or verification |
| codex/skill/SKILL.md | RELEASE | Reviewed public source, documentation or verification |
| core/MindOS.md | RELEASE | Reviewed public source, documentation or verification |
| core/templates/execution-observations.md | RELEASE | Reviewed public source, documentation or verification |
| core/templates/execution-stage-distillation.md | RELEASE | Reviewed public source, documentation or verification |
| core/templates/main-stage-distillation.md | RELEASE | Reviewed public source, documentation or verification |
| core/templates/profile-candidates.md | RELEASE | Reviewed public source, documentation or verification |
| core/templates/report.md | RELEASE | Reviewed public source, documentation or verification |
| core/templates/task.md | RELEASE | Reviewed public source, documentation or verification |
| docs/EXTERNAL_FIRST_USE_FEEDBACK.md | RELEASE | Reviewed public source, documentation or verification |
| docs/GITHUB_SECURITY_PLAN.md | RELEASE | Reviewed public source, documentation or verification |
| docs/INVENTORY.md | RELEASE | Reviewed public source, documentation or verification |
| docs/LICENSE_DECISION.md | RELEASE | Reviewed public source, documentation or verification |
| docs/LAUNCH_COPY.md | RELEASE | Three public-only copy drafts; no external posting |
| docs/OWNERSHIP.md | RELEASE | Reviewed public source, documentation or verification |
| docs/PLATFORM.md | RELEASE | Reviewed public source, documentation or verification |
| docs/PUBLIC_PRIVATE_BOUNDARY.md | RELEASE | Reviewed public source, documentation or verification |
| docs/QUICK_START.md | RELEASE | Reviewed public source, documentation or verification |
| docs/RELEASE_READINESS.md | RELEASE | Reviewed public source, documentation or verification |
| docs/SOURCE_MAP.md | RELEASE | Reviewed public source, documentation or verification |
| docs/VERIFY.md | RELEASE | Reviewed public source, documentation or verification |
| docs/asset-manifest.json | RELEASE | Reviewed public source, documentation or verification |
| examples/external-first-use-project/任务交接记录/README.md | RELEASE | Unexecuted synthetic example only |
| examples/external-first-use-project/当前有效/README.md | RELEASE | Unexecuted synthetic example only |
| examples/external-first-use-project/收件箱/EXT-FIRST-001_任务单.md | RELEASE | Unexecuted synthetic example only |
| examples/external-first-use-project/欢迎说明.md | RELEASE | Unexecuted synthetic example only |
| examples/external-first-use-project/规划与未决/README.md | RELEASE | Unexecuted synthetic example only |
| examples/external-first-use-project/项目当前阶段.md | RELEASE | Unexecuted synthetic example only |
| examples/external-first-use-project/项目总览.md | RELEASE | Unexecuted synthetic example only |
| examples/first-task.md | RELEASE | Reviewed public source, documentation or verification |
| presets/codex-workflow/README.md | RELEASE | Reviewed public source, documentation or verification |
| presets/full/README.md | RELEASE | Design-only; implementation DEFERRED |
| presets/minimal/README.md | RELEASE | Reviewed public source, documentation or verification |
| presets/observability/README.md | RELEASE | Design-only; implementation DEFERRED |
| tests/test_candidate.py | RELEASE | Reviewed public source, documentation or verification |
| tests/test_first_use.py | RELEASE | Reviewed public source, documentation or verification |
| tests/test_public_pretest.py | RELEASE | Reviewed public source, documentation or verification |
| tools/first_use_probe.py | RELEASE | Reviewed public source, documentation or verification |
| tools/history-distiller/README.md | RELEASE | Reviewed public source, documentation or verification |
| tools/history-distiller/distill.py | RELEASE | Reviewed public source, documentation or verification |
| tools/history-distiller/test_distill.py | RELEASE | Reviewed public source, documentation or verification |
| tools/prepublish_scan.py | RELEASE | Reviewed public source, documentation or verification |

DEFER: Runtime, Router, bot, File Bridge, Observers, launcher, daemon, plugin/store installer and private-history evidence. REMOVE_FROM_CANDIDATE: NONE. MIT LICENSE included; no formal tag or GitHub Release asset. Root .git metadata is not part of the tracked/public manifest. The provenance manifest excludes only its own content hash; tracked preflight compares exact staged bytes with the working tree and rejects extra files outside root Git metadata.
