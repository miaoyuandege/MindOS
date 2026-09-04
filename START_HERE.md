# Start here — AI-guided installation

**PUBLIC PRE-RELEASE TEST · NOT v0.1 FINAL · LICENSE PENDING · EXTERNAL FIRST-USE TESTING**

For the user: give this repository URL to your AI and say:

> 帮我安装 MindOS，并告诉我安装完成后怎么开始使用。

> Help me install MindOS, then tell me how to start using it.

The following steps are for that AI. Do the work your environment permits; do not make the user learn the internal workflow first. Reading this document does not grant new filesystem, credential, admin or background-execution permissions.

## A. Inspect before writing

1. Identify your actual tools, OS, supported client/version and target project. Tested baseline: Windows with native Codex CLI 0.149.1; other clients/platforms are not verified. Read [platform limits](docs/PLATFORM.md) when relevant.
2. If you can browse but cannot use local files or a terminal, say that installation is blocked by missing local capabilities. Ask the user to open a local-capable Codex task and give it the URL and request above; do not pretend a download or installation occurred.
3. Download/clone this public repository into a new, user-authorized location. Use the actual repository URL supplied by the user, not a guessed owner or private source. Do not reuse or overwrite an unrelated directory. Record the commit SHA when Git is available. Never ask for the maintainer's private files or account.
4. Establish the target project root; if none is chosen, offer the included [synthetic project](examples/external-first-use-project/项目总览.md). Only ask for a missing target/permission that changes the installation.
5. Inspect existing project-local and visible same-name `mindos` Skills. Do not overwrite unknown content or assume duplicate names merge. Explain the exact conflict and preserve the existing installation. Do not inspect credential stores or unrelated projects.

## B. Install the reviewed local Skill

Use the client's supported local Skill mechanism. The tested placement is `<project>/.agents/skills/mindos/SKILL.md`, copied from this repository's `codex/skill/SKILL.md`. This is a normal project file copy, not a global service install.

Use existing file tools or the non-overwriting PowerShell procedure in [Quick Start](docs/QUICK_START.md). Check source and destination first. No administrator privileges, registry changes, credential storage, daemon, watcher, database, Router, bot or Observer are required. Do not execute an unreviewed remote install script or change the user's account configuration.

## C. Place protocol and minimum context

Copy `core/` into a new `<project>/mindos-protocol/` so `MindOS.md` and its six template links remain together. Do not overwrite an existing protocol directory. Link or record `mindos-protocol/MindOS.md` in the existing project overview with the actual current-stage, Inbox and Handoffs locations. Preserve established project conventions; do not restructure a real project to fit the example.

For the included example, the overview already states these locations. Install the Skill and protocol there; no private author paths or additional systems are needed. The template directory is material to read, not a queue of tasks to execute.

## D. Verify honestly

- Confirm the current working root is the user's chosen project, not the downloaded distribution by mistake.
- Confirm the installed Skill and protocol match the reviewed source and are readable; check template links.
- Confirm the client discovers the project `mindos` Skill (CLI `/skills` or actual client listing). Explicitly select the project path if names collide. If reload is needed, say so; a file existing is not discovery evidence.
- Confirm the overview points to the installed protocol and actual project locations, with no maintainer-private path dependency.
- If any check fails, report the first divergence and smallest next action. No installation PASS without actual discovery. User acceptance and external first-use remain separate from these checks.

## E. Tell the user only the next useful step

After verified installation: “打开你的项目并说：接管这个项目。需要执行端继续时说：执行任务。” The exact command is `执行任务` without a trailing full stop. Explain advanced terms only when useful.

For the external trial, open `examples/external-first-use-project`, say “接管这个项目”, then “执行任务”. The prepared synthetic Task changes one sentence, verifies it, creates one report and preserves its Source. Expected duration is 5–10 minutes, a test-design target rather than measured performance. Do not pre-execute or mark it accepted on behalf of the tester.

Ask for only [short first-divergence feedback](docs/EXTERNAL_FIRST_USE_FEEDBACK.md). Never request raw sessions, prompt history, private code or credentials. Repository visibility and successful installation do not mean a final v0.1 release or external human first-use PASS.
