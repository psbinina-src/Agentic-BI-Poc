# Code Generation Plan — P1-U4 Gold Models, Samples, and Phase 2 Handoff

## Unit Context
- **Unit**: P1-U4 — Gold models, samples, and Phase 2 handoff.
- **Approved design**: build Gold sales, customer, and inventory models from accepted Silver, then publish sample query evidence and a Phase 2 handoff summary.

## Generation Steps
### Step 1 — Configuration and orchestration
- [x] Confirm Silver input contract and the final Gold output configuration.
- [x] Set the local output path and final handoff metadata.

### Step 2 — Implement Gold transformations
- [ ] Create `src/p1_u4/config.py` for Gold paths and model metadata.
- [ ] Create `src/p1_u4/gold.py` to derive the final Gold sales, customer, and inventory tables.
- [ ] Add deterministic measures and dimension joins from the accepted Silver tables.

### Step 3 — Sample query and reporting
- [ ] Create `src/p1_u4/queries.py` for business sample queries on sales trends, repeat purchase, and inventory risk.
- [ ] Publish the evidence outputs in a local results directory.

### Step 4 — CLI and validation
- [ ] Create `src/p1_u4/cli.py` to run the Gold transformation and sample queries.
- [ ] Return a nonzero exit code on invalid upstream Silver data or blocked quality gates.

### Step 5 — Focused tests
- [ ] Add `tests/p1_u4/test_gold.py` for Gold fact/dimension generation.
- [ ] Add `tests/p1_u4/test_queries.py` for sample query outputs.
- [ ] Add `tests/p1_u4/test_cli.py` for CLI success/failure behavior.

### Step 6 — Final readiness
- [ ] Verify the Gold layer against the Phase 2 handoff contract.
- [ ] Record the final handoff evidence and completion status.
