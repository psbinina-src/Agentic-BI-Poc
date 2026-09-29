# Unit Test Instructions — Phase 2 Gold REST API

## Focused P2-U2 Tests
Run from the repository root:

```powershell
py -m pytest tests/p2_u2 -q
```

These tests use temporary synthetic Parquet fixtures and cover catalogue/schema metadata, documented relationships, safe projections and filters, ISO date values, grouped aggregations, joins, row limits, unavailable datasets, and rejection of unsafe inputs.

## Full Project Test Suite

```powershell
py -m pytest -q
```

The full suite includes Phase 1 Gold/lakehouse tests, the P2-U1 reference tests, Phase 2 API tests, and the Phase 4 dashboard contract tests.
