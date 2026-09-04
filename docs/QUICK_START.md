# Your first scoped change

If an AI is installing this for you from a URL, start with [START_HERE](../START_HERE.md). The procedure below is the implementation reference for that AI, not prerequisite homework for the tester. The [synthetic project](../examples/external-first-use-project/项目总览.md) is an available target if you have not selected a real project.

For someone who already uses Codex with an authorized local project. This candidate supplies workflow files, not Codex, authentication or a server. Aim: understand it in ten minutes and try a small change in thirty; these are goals, not measured timing guarantees.

## 1. Review and place the files

Review [the Skill](../codex/skill/SKILL.md) and [protocol](../core/MindOS.md). From the project root in PowerShell 7, set `$candidatePath` to your downloaded candidate directory. The following copies only the reviewed Skill/protocol/templates and refuses to overwrite an existing installation:

```powershell
$candidatePath = Read-Host 'Path to the reviewed MindOS candidate'
$skillTarget = Join-Path (Get-Location) '.agents/skills/mindos'
$protocolTarget = Join-Path (Get-Location) 'mindos-protocol'
if ((Test-Path -LiteralPath $skillTarget) -or (Test-Path -LiteralPath $protocolTarget)) {
    throw 'Existing installation: review and merge deliberately; do not overwrite.'
}
$skillSource = Join-Path $candidatePath 'codex/skill'
$coreSource = Join-Path $candidatePath 'core'
if (-not (Test-Path -LiteralPath (Join-Path $skillSource 'SKILL.md')) -or
    -not (Test-Path -LiteralPath (Join-Path $coreSource 'MindOS.md'))) {
    throw 'Candidate files are missing.'
}
New-Item -ItemType Directory -Path $skillTarget | Out-Null
Copy-Item -LiteralPath (Join-Path $skillSource 'SKILL.md') -Destination $skillTarget
Copy-Item -LiteralPath $coreSource -Destination $protocolTarget -Recurse
```

In your existing project overview, link `mindos-protocol/MindOS.md` and identify the actual overview, current-stage, Inbox and Handoffs locations. Preserve existing conventions; do not create a Runtime or restructure the project. If no overview exists, ask the AI to establish a minimal one with you. New users need only know the goal and allowed files.

## 2. Open and take over

Open Codex at that project root. In CLI, use `/skills` to check that `mindos` points to the project installation. If it is missing, check the location and restart the client. If multiple same-name entries appear, explicitly choose the project path; do not assume they merge. See [the supported mechanism](https://learn.chatgpt.com/docs/build-skills).

Say “接管这个项目” (or “Take over this project”); explicitly select `$mindos` if automatic matching does not select it. The AI should read the linked protocol and existing overview/stage, restore evidence and ask only for consequential gaps. Do not accept a claim that inaccessible files were read.

## 3. Complete one small task

Choose an authorized documentation change, following [the first-task example](../examples/first-task.md). Give one allowed file, exact expected text and a simple verification. Put the reviewed Task in the project's known Inbox, or provide it directly if no Inbox workflow exists. No Router is needed.

Say “执行任务”. Inspect the edited file and single report. Original Source belongs unchanged in the agreed Handoffs location after reporting. Accept it or request a focused Rework; technical checks do not replace your acceptance.

## Limitations and troubleshooting

Local project Skill discovery was verified with native CLI 0.149.1; clean authenticated AI execution and report generation are still pending. Do not treat this guide as a measured first-user success. [Platform contract](PLATFORM.md) and [release status](RELEASE_READINESS.md) explain the remaining gate.

Missing client/login: install or sign in through your existing trusted client workflow; do not copy another user's account files or secrets. Missing protocol: fix the overview link. Missing permissions: stop only the affected action. Duplicate Skill: select the intended project path. No Runtime: use manual mode. No file artifact capability: disclose it and use reviewed text.

Optional later: paste the [generic account router](../chatgpt/custom-instructions/generic.md) into ChatGPT yourself; that separate optional artifact has no claimed account-save verification. [Offline history analysis](../tools/history-distiller/README.md) is not needed for first use and must stay private.
