# Provenance / third-party audit

Scope: the exact paths in asset-manifest.json plus that manifest itself. This is a source-provenance review, not a legal opinion or a warranty of worldwide copyrightability.

| Assets | Inspected provenance | Distribution conclusion |
| --- | --- | --- |
| core/MindOS.md; codex/skill/SKILL.md; codex/profiles/guardrails.md; generic account router | Curated from project-controlled internal governance, with explicit transformations recorded in SOURCE_MAP and manifest | Candidate-authored/maintained content; no identified copied third-party prose; owner's licensing authority still requires confirmation |
| Six core/templates files | Unfilled internal generic templates, no user-completed content | No identified third-party notice obligation |
| History distiller and tests | Project-controlled parser and synthetic fixtures; imports only argparse, collections, datetime, hashlib, json, pathlib, re and standard test modules | Python standard library is referenced, not bundled; no upstream source package or private verification module included |
| Preflight, local-discovery probe and candidate tests | New local tooling; standard library only; public API requests authored from documented contracts, not copied SDK code | No bundled SDK, client executable or third-party runtime; Codex remains separately installed |
| README/docs/security/contributing/presets/example/gitignore | New candidate prose and links; summaries of official sources, not full copied articles | No image, font, binary, model weight, license text or external repository source imported |

Review method: per-file mapping plus imports, textual attribution/URL search, fixture inspection and accepted source-creation evidence. No external repository clone or automatic private-tree export was used. Synthetic test strings are not real accounts or histories. Absence of a notice in source alone is not proof of unrestricted ownership; externally sourced additions must be re-audited.

No redistributable third-party component requiring a separate THIRD_PARTY_NOTICES.md was identified, so no empty notice file is created. MIT/Apache compatibility has no known third-party conflict in this inventory; final license and owner attribution remain explicit user decisions. AI assistance does not by itself prove originality or legal title.
