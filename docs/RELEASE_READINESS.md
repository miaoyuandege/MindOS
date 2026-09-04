# v0.1 release-readiness: PARTIAL

Public-pretest update: a separately authorized public repository is the external first-use entry, via [START_HERE](../START_HERE.md). This changes the old private-package-first route, not the final-release gates. A public pretest is allowed while License and external human first-use remain pending; no formal tag or GitHub Release is authorized. The matrix below concerns final v0.1 readiness, not permission for the pretest.

Intended version: 0.1.0-rc1. This is a mutable local preparation snapshot, **not a frozen release candidate**. Baseline bootstrap has been accepted; this new release-readiness delta still requires its own main-AI acceptance.

| Gate | State |
| --- | --- |
| Product scope / inventory | YES: Codex-first local governance, exact file dispositions in INVENTORY.md |
| README / onboarding documentation | YES: concrete repo-local setup, no timing guarantee |
| Clean-environment first use | NO: local Skill discovered; outside-workspace metadata and absent isolated login prevent a clean AI Task/Report claim |
| Skill distribution | YES for manual local placement/discovery; plugin/store installer not shipped |
| Ownership / third-party review | Provenance reviewed; no identified third-party notice obligation; owner authority/attribution confirmation pending with license |
| Security / contribution plan | YES as contingent documents; no live reporting channel claimed |
| License | NO: user decision pending; no LICENSE file |
| Exact candidate freeze | NO: first-use gate is unresolved, not merely license/publish choice |
| Ready for GitHub Publish Task | NO |

Run the [verification checks](VERIFY.md) on the exact snapshot and inspect their actual results; documentation does not substitute for fresh hash/privacy evidence.

Next: complete the first-use trial in a truly isolated, authenticated user environment, select license/attribution and obtain main-AI acceptance. Then recheck inventory, ownership, privacy, links and tests; freeze all release files with per-file and aggregate SHA256, environment and timestamp. Do not manufacture a conditional LICENSE-only freeze while clean first use is pending.

[License packet](LICENSE_DECISION.md), [ownership audit](OWNERSHIP.md), [platform contract](PLATFORM.md), [security plan](GITHUB_SECURITY_PLAN.md). Git repository creation, remotes, commit, push, tag and release require separate explicit publication authority. None is performed by these tools.

The generic account router remains independent of any maintainer's private account instructions. Do not publish private reports or the local first-use workspace. Observer/full presets remain design-only; no background modules are enabled.
