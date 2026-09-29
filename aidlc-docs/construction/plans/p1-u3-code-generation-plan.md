# Code Generation Plan — P1-U3 Silver Standardization and Data Quality

## Unit Context
- **Unit**: P1-U3 — Silver standardization and data quality.
- **Approved design**: local-first typed Silver transformation from accepted Bronze outputs and explicit quality gate publication.
- **Owner**: one data engineer.

## Project Structure
```text
src/
  p1_u3/
    __init__.py
    config.py
    transform.py
    quality.py
    cli.py

tests/
  p1_u3/
    test_transform.py
    test_quality.py
    test_cli.py
```

## Generation Steps
### Step 1 — Configuration and orchestration
- [x] Confirm the local Bronze input contract and target Silver output paths.
- [x] Set up the typed Silver configuration object and local run metadata.
- [x] Keep runtime output under `lakehouse/silver/`.

### Step 2 — Implement transformation logic
- [ ] Create `src/p1_u3/config.py` for Bronze and Silver path configuration.
- [ ] Create `src/p1_u3/transform.py` to standardize Bronze entities into typed Silver tables.
- [ ] Retain lineage columns and stable keys from Bronze.
- [ ] Convert raw source values to typed values without inventing new business semantics.

### Step 3 — Implement the quality gate
- [ ] Create `src/p1_u3/quality.py` for required-field, type, duplicate, null, domain, and referential checks.
- [ ] Publish a pass/fail quality report that records the failing rule names and counts.
- [ ] Make critical failures blocking before any Gold work begins.

### Step 4 — CLI and validation
- [ ] Create `src/p1_u3/cli.py` to run the transform and quality gate.
- [ ] Return nonzero exit on critical quality failures.
- [ ] Print the output paths and summary of the quality report.

### Step 5 — Focused tests
- [ ] Add `tests/p1_u3/test_transform.py` for successful transformation behavior.
- [ ] Add `tests/p1_u3/test_quality.py` for fail-fast quality checks.
- [ ] Add `tests/p1_u3/test_cli.py` for CLI pass/fail behavior.

### Step 6 — Final unit readiness
- [ ] Verify the implementation against the approved Silver contract.
- [ ] Confirm downstream Gold readiness and contract evidence.
