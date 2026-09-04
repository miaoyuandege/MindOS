# MindOS

**PUBLIC PRE-RELEASE TEST · NOT v0.1 FINAL · LICENSE PENDING · EXTERNAL FIRST-USE TESTING**

## Install with AI / 让 AI 帮你安装

Give this repository URL to your AI and say:

> 帮我安装 MindOS，并告诉我安装完成后怎么开始使用。

> Help me install MindOS, then tell me how to start using it.

**AI: read [START_HERE.md](START_HERE.md) first.** It guides environment checks, a safe project-local Skill/protocol installation, actual verification and the next user action. Users do not need to learn Skill paths or workflow terminology first.

MindOS is a Codex-first local workflow and governance layer for long-running AI projects.

It helps an AI recover project context, carry out scoped work, preserve evidence, and distinguish implementation from verification and acceptance. It is not an autonomous operating system, a background worker, a hosted service, or a promise about any model's capabilities.

This is public pre-release test source, not a licensed final open-source release, stable product or production-readiness claim. License/owner attribution and clean authenticated external first-use remain pending. Local Skill discovery is verified, not end-to-end onboarding.

## Start small

For someone who already uses Codex with an existing local project:

1. Read the [short quick start](docs/QUICK_START.md).
2. Follow the concrete PowerShell repo-local setup in the quick start: reviewed [Skill](codex/skill/SKILL.md) → `.agents/skills/mindos`, protocol → project overview. No personal configuration or installer is required.
3. Open your project and say “Take over this project” (or “接管这个项目”). Let the AI locate its trusted project files before changing anything.
4. Discuss your goal normally. In the execution task, say “执行任务” to continue the scoped worklist. Missing context or permission should be explained, not guessed.

Aim: understand the workflow in about ten minutes and try one small useful change within thirty. These are onboarding goals, not measured guarantees. You do not need a database, server, bot, or multi-agent setup for the first use.

## Included

- [Protocol and templates](core/MindOS.md): roles, evidence, scoped work and lifecycle guidance.
- [Codex execution Skill](codex/skill/SKILL.md) and [native Agent guardrails](codex/profiles/guardrails.md).
- [Thin generic account router](chatgpt/custom-instructions/generic.md), optional; full rules stay in external MindOS.md. Account save is not yet verified.
- [Offline history distiller](tools/history-distiller/README.md), optional; source and synthetic tests only. Its generated outputs remain private.
- Presets: [minimal](presets/minimal/README.md), [codex-workflow](presets/codex-workflow/README.md), [observability](presets/observability/README.md), [full](presets/full/README.md). The last two are design-only, not installable bundles.
- [Ready-to-try synthetic project](examples/external-first-use-project/项目总览.md), [short feedback](docs/EXTERNAL_FIRST_USE_FEEDBACK.md), and a [generic first-task example](examples/first-task.md).

## Maintainers

[Platform](docs/PLATFORM.md) · [Inventory](docs/INVENTORY.md) · [License decision](docs/LICENSE_DECISION.md) · [Ownership](docs/OWNERSHIP.md) · [Security](SECURITY.md) · [Contributing](CONTRIBUTING.md).

[Public/private boundary](docs/PUBLIC_PRIVATE_BOUNDARY.md) → [source map](docs/SOURCE_MAP.md) → [local verification](docs/VERIFY.md) → [release-readiness blockers](docs/RELEASE_READINESS.md).

The public pretest is specifically for independent first-use feedback. No v0.1 tag, GitHub Release, package-registry release, final license or synchronization daemon is included. Do not turn a successful download into a claim of external human acceptance.
