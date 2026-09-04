# GitHub-side plan — not executed

The public pretest has separate upload authorization; final v0.1 still requires license and external first-use evidence. Verify actual settings during that pretest task and record their current state in its report. The checklist itself is not proof that any feature is enabled.

2026-09-04 repository API check: secret scanning ENABLED; repository push protection ENABLED; private vulnerability reporting ENABLED. No claim is made about tested notification delivery, branch rules, required CI or Dependabot updates. Private reporting policy is in SECURITY.md. These controls supplement the exact local pre-push scan, not replace it.

1. Re-run local privacy review on the exact frozen source before the first upload. GitHub scanning is a second layer, not permission to upload questionable files.
2. Confirm public-repository secret scanning status and alert routing. GitHub documents automatic free scanning of public repositories. See [secret scanning](https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning).
3. Confirm both account and repository push-protection configuration and available plan features. Do not assume repository protection is enabled because user-level protection is. Do not bypass a block merely to complete a release. See [push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection).
4. Enable Private Vulnerability Reporting, check the private form and maintainer notifications, then remove the contingent wording from SECURITY.md only after verification. No fake contact address. See [configuration](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository).
5. Consider default-branch rules appropriate to actual maintainers: block deletion/force-push; require the verification checks once real CI exists. Do not advertise required CI or approval rules before they are configured.
6. Enable available dependency alerts where dependency manifests exist. This candidate has only standard-library Python tools and bundles no runtime dependencies; do not invent a package manifest or scheduled update workflow solely to enable Dependabot.
7. Record actual settings, recipients and limitations in the release report without secret values. Any later source or license change invalidates the old candidate identity.

Secrets accidentally disclosed require a separately authorized response/rotation; this task does not rotate credentials or change user accounts.
