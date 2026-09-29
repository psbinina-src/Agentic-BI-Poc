# Code Generation Plan — P1-U1 Synthetic Generator and Source Contract

## Unit Context
- **Unit**: P1-U1 — Synthetic generator and source contract.
- **Story**: P1-US-1 — reproducibly generate synthetic source data and provide stable inputs for Bronze.
- **Accountable owner**: One data engineer; execute all steps sequentially.
- **Dependencies**: None; P1-U1 is first in the approved unit chain.
- **NFR/Functional design**: Five valid synthetic entities; fixed defaults (seed 42, 2023-01-01 through 2025-12-31 inclusive, about 10,000 customers, 1,000 products, 100,000 lines); daily snapshots; in-memory generation; fail-fast/no-retry; direct file output, success manifest last, partial/unmanifested files invalid.
- **Stories / handoff**: P1-US-1; output CSV schemas, keys, manifest, configuration and sample evidence for P1-U2.
- **Project state**: Greenfield multi-unit monolith; current runtime is Python 3.14.4. Code belongs in the workspace root, not `aidlc-docs/`.

## Planned Project Structure

```text
pyproject.toml
.gitignore
config/
  p1-u1-defaults.toml
src/
  p1_u1/
    __init__.py
    __main__.py
    models.py
    config.py
    generator.py
    validation.py
    csv_writer.py
    manifest.py
    cli.py
tests/
  p1_u1/
    test_config.py
    test_generator.py
    test_validation.py
    test_outputs.py
    test_cli.py
lakehouse/
  source/                 # generated CSVs and manifest; ignored runtime data
```

Python and TOML configuration use the standard library. Pytest is a development/test dependency only. Source files and manifests are generated at runtime and are not committed.

## Numbered Generation Steps

### Step 1 — Scaffold Unit and Project Metadata
- [x] Create `pyproject.toml` with Python `>=3.11` (for standard-library `tomllib`), package metadata, and optional test dependency `pytest>=9,<10`.
- [x] Create `.gitignore` entries for Python caches, virtual environments, pytest cache, and runtime lakehouse layer data (`lakehouse/source/`, `lakehouse/bronze/`, `lakehouse/silver/`, `lakehouse/gold/`).
- [x] Create package/test directories according to the greenfield multi-unit monolith structure: `src/p1_u1/` and `tests/p1_u1/`.
- [x] Add `config/p1-u1-defaults.toml` with the approved seed, inclusive date range, dataset defaults, and output path.
- [x] Add package entry points (`__init__.py`, `__main__.py`) needed to run the local module CLI.
- [x] Verify editable local installation from `pyproject.toml`; package import reports version `0.1.0`.

### Step 2 — Implement Typed Source Models and Configuration
- [x] Create `src/p1_u1/models.py` for Customer, Product, OrderHeader, OrderLine, InventorySnapshot, GenerationManifest/RunResult models.
- [x] Create `src/p1_u1/config.py` to read TOML defaults, apply CLI overrides, resolve `lakehouse/source/`, and validate dates/positive volumes before generation.
- [x] Preserve functional-design identifiers, field sets, fixed defaults, scenario metadata, and schema version.

### Step 3 — Implement Deterministic In-Memory Generation
- [x] Create `src/p1_u1/generator.py` to build entities in dependency order using seed 42 by default and stable IDs/order.
- [x] Produce exactly the configured order-line count; derive order headers by grouping one or more lines per order.
- [x] Generate one inventory snapshot per product per inclusive calendar day.
- [x] Include repeat-customer, time/region/category variation, and low-stock/high-velocity scenarios deterministically.
- [x] Keep all entity collections in memory per the approved design; do not add streaming, retries, or external fake-data services.

### Step 4 — Implement Source Validation
- [x] Create `src/p1_u1/validation.py` for required entity/count checks, unique IDs, foreign-key relationships, domain/date constraints, and required scenario presence.
- [x] Return inspectable validation outcomes; a failed check blocks output publication and causes a nonzero CLI result.
- [x] Do not generate invalid test fixtures; test invalid configurations or validator conditions with small test-created objects only as required for ordinary unit tests.

### Step 5 — Implement CSV Output and Manifest-Last Publication
- [x] Create `src/p1_u1/csv_writer.py` to write five UTF-8 CSVs with stable header/row order and ISO dates/canonical numeric formatting directly under the configured source paths.
- [x] Create `src/p1_u1/manifest.py` to record schema version, effective config, counts, paths, checksums, scenario/validation results, and operational run time.
- [x] Publish the success manifest only after all CSV files have been written and checks pass.
- [x] On validation or file failure, return a failure and do not publish a success manifest; leave partial/unmanifested files as selected. Do not add temp promotion, backup, cleanup, or automatic retry logic.

### Step 6 — Implement CLI and Run Summary
- [x] Create `src/p1_u1/cli.py` with a generator command, TOML defaults plus command-line overrides for seed/date/size/output path, and actionable errors.
- [x] Report effective settings, per-entity row counts, elapsed duration, output paths, manifest path on success, and failure status on error.
- [x] Ensure module invocation through `python -m p1_u1` works after the documented editable local install.

### Step 7 — Add Conventional Tests
- [x] Add `tests/p1_u1/test_config.py` for defaults, overrides, date/volume validation, and invalid configuration failure.
- [x] Add `tests/p1_u1/test_generator.py` using small settings to verify same-config determinism, stable IDs, exact line counts, relationship integrity, and required scenario presence.
- [x] Add `tests/p1_u1/test_validation.py` for valid data and selected invalid object/config cases without introducing generated negative fixtures.
- [x] Add `tests/p1_u1/test_outputs.py` for CSV headers/order/format, checksums, manifest-last behavior, and no success manifest when a simulated write/validation failure occurs.
- [x] Add `tests/p1_u1/test_cli.py` for successful invocation, reported counts/duration, and nonzero failure behavior. `python -m pytest -q`: 18 passed.

### Step 8 — Document U1 Source Contract and Usage
- [x] Create `aidlc-docs/construction/p1-u1/code/generation-guide.md` with prerequisites, setup/test commands, generation command, defaults, overrides, output paths, and regeneration behavior.
- [x] Create `aidlc-docs/construction/p1-u1/code/source-schema.md` with entity grains, fields, IDs/relationships, CSV format, manifest contents, and failed-run caveat for P1-U2.
- [x] Ensure documentation explains that default full output includes 1,096,000 inventory snapshots, in-memory generation can consume substantial memory, and no hard performance limit is promised.

### Step 9 — Code Generation Summary and Readiness
- [x] Summarize created application files under workspace root and documentation under `aidlc-docs/construction/p1-u1/code/code-generation-summary.md`.
- [x] Confirm P1-US-1 and P1-U1 handoff coverage; P1-U2 must require a valid success manifest and matching checksums. P1-U2 remains blocked until P1-U1 code review/approval and sequential contract evidence.
- [x] Update this plan and `aidlc-docs/aidlc-state.md` as steps are completed.

## Scope Exclusions
- No Bronze ingestion, DuckDB transformation, Parquet output, Silver/Gold model, or downstream CLI commands; these belong to P1-U2 through P1-U4.
- No network/API/server process, external data generator, UI, scheduled workflow, or infrastructure deployment.
- Full default-volume execution and end-to-end validation are reserved for the approved Build and Test stage; unit tests use small configurable datasets.

## Approval Gate
This is the single source of truth for P1-U1 Code Generation. Review the complete plan and approve the steps before any application code or tests are created. Request Changes or Approve & Continue to Code Generation for P1-U1.
