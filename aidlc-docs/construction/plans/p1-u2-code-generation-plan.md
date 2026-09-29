# Code Generation Plan — P1-U2 Bronze Ingestion and Lineage

## Unit Context
- **Unit**: P1-U2 — Bronze ingestion and lineage.
- **Story**: P1-US-1 — ingest reproducible synthetic inputs as stable, traceable Bronze data.
- **Owner**: One data engineer; sequential execution only.
- **Approved design**: local-first DuckDB ingestion from validated source CSVs into Bronze Parquet with manifest checksum gates and row-level lineage metadata.

## Project Structure
```text
pyproject.toml
src/
  p1_u2/
    __init__.py
    config.py
    ingest.py
    validation.py
    cli.py
tests/
  p1_u2/
    test_ingest.py
    test_validation.py
    test_cli.py
lakehouse/
  bronze/
  source/
```

## Numbered Generation Steps
### Step 1 — Scaffold and package metadata
- [x] Confirm the project root and source layout for the unit.
- [x] Add local package modules under `src/p1_u2/`.
- [x] Keep runtime outputs under `lakehouse/` and do not commit generated Bronze data.

### Step 2 — Implement configuration and manifest validation
- [x] Create `src/p1_u2/config.py` to hold the Bronze source path, output path, and run ID configuration for local ingestion.
- [x] Create `src/p1_u2/validation.py` to verify the source contract: file presence, manifest presence, checksum match, entity completeness, and valid source status.
- [x] Implement explicit validation errors for missing manifests, invalid checksum, missing entities, and invalid manifest state.

### Step 3 — Implement the raw Bronze loader
- [x] Create `src/p1_u2/ingest.py` to read each accepted source CSV with DuckDB.
- [x] Append lineage metadata: `source_file`, `source_row_number`, `source_run_id`, `ingested_at`.
- [x] Write each entity as a Bronze Parquet file under `lakehouse/bronze/`.
- [x] Keep all transformation work raw and non-semantic; no Silver transformations are included here.

### Step 4 — Implement CLI and local execution
- [x] Add `src/p1_u2/cli.py` to run the ingestion from a source path and bronze path.
- [x] Print a clear success summary with output paths and row counts.
- [x] Return a nonzero exit code for invalid source manifests or checksum mismatches.

### Step 5 — Add conventional tests
- [x] Add `tests/p1_u2/test_ingest.py` for successful ingest, lineage metadata, and checksum mismatch rejection.
- [x] Add `tests/p1_u2/test_validation.py` for source manifest/file validation edge cases.
- [x] Add `tests/p1_u2/test_cli.py` for command-line success and failure behavior.

### Step 6 — Final unit readiness
- [x] Verify the implementation against the approved Bronze contract and P1-U2 design artifacts.
- [x] Update the plan and `aidlc-docs/aidlc-state.md` as code is completed.
- [x] Confirm the unit is ready for the P1-U2 Build and Test stage.

## Scope Guardrails
- No Silver or Gold transformations are included.
- No external services are introduced.
- No Docker or container dependency is required.
- Only validated raw source files are allowed into Bronze.
