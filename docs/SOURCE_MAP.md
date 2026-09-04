# Explicit source map

Discoverability delta: docs/LAUNCH_COPY.md is NEW_PUBLIC, authored from public product positioning only; no private history or evidence is copied. README adds a short problem statement and illustrative before/after flow, not new product behavior. Social-preview production files are kept outside the Git tree for a separate settings upload.

MIT activation delta: [LICENSE](../LICENSE) uses the [standard MIT text](https://choosealicense.com/licenses/mit/) with only the year/fullname placeholders filled as 2026 miaoyuandege by user decision. License state, inventory, manifest and directly affected verification are synchronized; protocol, Skill and onboarding behavior are unchanged.

Public-pretest delta: START_HERE.md, EXTERNAL_FIRST_USE_FEEDBACK.md, the synthetic external-first-use project and tests/test_public_pretest.py are NEW_PUBLIC; no private Task or filled Report is copied. README/docs now distinguish authorized public testing from final v0.1 licensing/readiness. The preflight adds exact-index scanning for the authorized Git workflow; tracked bytes must match the reviewed working tree and manifest. No private parent repository or real task source is imported.

This is a local pre-release candidate, not a final release or a new internal authority. Synchronization is manual: select → inspect → transform → verify → update manifest. Never copy a private workspace and then remove files.

Root aliases refer to the maintainer's private checkout; their machine-specific values are deliberately not distributed. GLOBAL = internal global governance root; PROJECT = internal project governance root; PROGRAMS = internal shared tooling root. Public paths are relative to this candidate tree.

| Public asset | Internal canonical source / origin | Transformation and sync rule | Verification |
| --- | --- | --- | --- |
| core/MindOS.md | GLOBAL/MindOS.md | Curated generic protocol, including Lifecycle Delta; strip local paths, personal projects, routing configuration and private Evidence links; do not blindly mirror | Role/authority/lifecycle walkthrough, link/privacy scan |
| core/templates/*.md | GLOBAL/模板; exact per-file mapping in asset-manifest.json | Only six inspected generic Task/Report/four Stage Source templates; no filled-in documents | Inventory and privacy scan |
| codex/skill/SKILL.md | PROJECT/核心区/MindOS_v4.1/执行AI-Skill/SKILL.md | Generic project-relative execution subset; no machine-specific Runtime or installed path; retain safety and manual completion | Skill validator + protocol consistency |
| chatgpt/custom-instructions/generic.md | GLOBAL/用户画像/Custom Instructions/Custom Instructions v5 Account.md | Thin generic account router; full v5 remains internal design reference, full protocol stays external; remove private path/preferences | Role separation, length and four scenario walkthroughs; actual account save separate |
| codex/profiles/guardrails.md | GLOBAL/开发模式.md | Stable native discipline only; no personal model observations, private task IDs, fixed model/effort/cost claims | Evidence boundary review |
| tools/history-distiller/distill.py | PROGRAMS/tools/codex-history-distiller/distill.py | Generic source; require explicit date range instead of private study defaults; no real logs/output bundled | Synthetic focused tests |
| tools/history-distiller/test_distill.py | PROGRAMS/tools/codex-history-distiller/test_distill.py | Synthetic projects/models only; omit test of internal-only verify_evidence module (that module binds private Evidence and is DEFERRED) | Ten portable synthetic tests |
| README.md, docs/*, presets/*, examples/*, tools/prepublish_scan.py, tests/*, tools/history-distiller/README.md, .gitignore | New public-only docs / preflight / synthetic tests | Written specifically for this workspace; no internal data copied | Manifest coverage, links, focused tests, pre-publish scan |

Lifecycle sync point: internal protocol and local CI v5/Skill are available after the Lifecycle implementation attempt. This candidate consumes the generic stable Delta, not an assertion of Main AI Acceptance or account synchronization. On the next approved Delta, inspect these exact canonical sources, reapply transformations, compare public diffs, run focused tests and preflight, and record public hashes. Do not change internal sources from this directory.

DEFER: Local File Bridge, Git/System/Runtime observers, Inbox Router and one-click launcher. Their current implementations/configs bind local roots, production profiles or internal evidence. Bootstrap does not refactor or package them. No Runtime DB, real session, deployment config, user profile, screenshots, generated observations or live Task/Report is part of the distribution.

Every current file is enumerated in [asset-manifest.json](asset-manifest.json). The manifest excludes only itself to avoid recursive hashing; unlisted files fail preflight. Public hashes describe this mutable snapshot, not a final v0.1 freeze.

Release-readiness delta: SECURITY.md, CONTRIBUTING.md, docs/LICENSE_DECISION.md, docs/OWNERSHIP.md, docs/PLATFORM.md, docs/GITHUB_SECURITY_PLAN.md, docs/INVENTORY.md, tools/first_use_probe.py and tests/test_first_use.py are NEW_PUBLIC. Documentation cites official pages with short paraphrases. The probe is new stdlib-only local discovery tooling; no SDK code, account/configuration, upstream executable or private metadata is redistributed. Existing README/Quick Start/preflight/tests receive only the associated onboarding, public-reference classification and verification changes. Generic Skill/protocol semantics remain unchanged. Internal baselines are accepted; acceptance of this new readiness delta remains separate.
