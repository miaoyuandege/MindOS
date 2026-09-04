# Optional offline history distiller

Standard-library Python parser, tested with synthetic JSONL only in this public tree. It extracts allowlisted metadata, separates requested/effective receipts and preserves fixed-prefix replay evidence. It never calls a model, shell or network service.

Local analysis is not public data: generated reports/manifests include session identifiers, workspace paths, task labels and usage metadata. They are **private**, not anonymized. Supply only explicitly authorized input roots and place output outside this distribution. No real history, private verification script or generated observations are bundled.

From this folder, run the synthetic checks:

```text
python -B -m unittest test_distill -v
```

CLI inputs are explicit: `--sessions-root`, `--archived-root`, `--from-date`, `--to-date`, `--output`; optional `--project` and `--manifest`. Dates currently use a documented fixed UTC+08:00 day boundary (inherited parser semantics), not your system timezone. Output must be new and must not overlap inputs or protected agent-data directories. Do not pass private paths in a public issue.

This is historical observation, not billing, causal performance comparison, task completion or acceptance. Real schema changes require new focused evidence; fixture model names are synthetic labels, not supported model recommendations. Source provenance is reviewed in the candidate ownership document; final license and release gates remain pending.
