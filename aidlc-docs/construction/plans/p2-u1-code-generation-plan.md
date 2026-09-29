# P2-U1 Code Generation Plan — Gold Contract and Semantic Catalog

## Unit Context
- **Story**: P2-US-1 — discover governed metrics and dimensions over Gold.
- **Approved functional design**: `aidlc-docs/construction/p2-u1/functional-design/`.
- **Approved unit boundary**: `aidlc-docs/inception/application-design/p2/units/unit-of-work.md`.
- **Dependency**: Phase 1 Silver/Gold pipeline. P2-U2 remains blocked until this unit's handoff passes.
- **Owner**: One data engineer, sequential work.
- **Implementation style**: Minimal diff to existing Python/DuckDB Gold code and focused tests; one small version-controlled Cube Core project under `semantic/cube/`.

## Hard Runtime Constraint
The approved requirement prohibits Docker, WSL, and hosted semantic services. Cube's official self-hosted quickstart documents Docker Compose, but its published Apache-2.0 npm server and DuckDB driver also expose a native Node server path. **Step 1 was used as a blocking feasibility spike.** Do not add container setup, run Cube through Docker, or silently substitute another semantic platform. Native API/query feasibility passed on this Windows host. The spike did reveal that Cube Core 1.7.47 binds HTTP/SQL (and its local Cube Store helper) to wildcard addresses, with dev mode bypassing auth; loopback-only binding is not present in the inspected server path. Keep the development process stopped. Resolve a safe local-access approach before P2-U2 service implementation; do not use dev mode as the runnable service configuration.

## Numbered Generation Steps

### Step 1 — Native Cube Core + DuckDB Feasibility (P2-US-1)
- [x] Check installed Node/npm and Python/DuckDB toolchain availability. Node 24.21.0, npm 11.19.0, Python 3.14.4; `pytest` is not available on PATH (use the project's Python environment/module invocation during testing).
- [x] Verify the selected Cube Core server and DuckDB driver versions, open-source license, and documented native host startup path (no Docker/WSL). `@cubejs-backend/server` and `@cubejs-backend/duckdb-driver` 1.7.47 are Apache-2.0; `cubejs-server` has native `dev-server` and `server` commands. The server and DuckDB Node driver loaded on Windows x64.
- [x] In a disposable local test, prove Cube can query one Phase 1 Gold Parquet file through DuckDB and serve one governed query locally. Catalog `/v1/meta` returned the Sales model; REST `Sales.netSales` query succeeded from the local `sales_gold.parquet` (DuckDB read_parquet).
- [x] Record the exact version, commands, config, and pass/fail evidence in this feasibility plan and the P2-U1 handoff summary.
- [x] **Stop condition evaluated**: native runtime and direct local Parquet access were proven, so Cube-dependent P2-U1 work may continue. Stop/decision gate remains for safe service access because Cube bound test ports to `0.0.0.0`/`::` and development mode disabled auth. No development server is left running.

### Step 2 — Correct Existing Gold Contract (P2-US-1)
- [x] Modify `src/p1_u4/gold.py` in place: filter sales to completed orders; expose order `channel` in `sales_gold`; derive product-day demand from completed order-line units over `[snapshot_date - 30 days, snapshot_date)`; divide by a fixed 30 days; calculate coverage and the `calculated` / `no_demand` status fields.
- [x] Preserve existing Gold filenames and grains. Do not add forecast measures.
- [x] Keep low-stock calculation and all existing unrelated fields stable.

### Step 3 — Focused Gold Tests (P2-US-1)
- [x] Extend `tests/p1_u4/test_gold.py` with completed-vs-cancelled orders, distinct order-line/order behavior, sales channel, demand lookback boundary (include day -30; exclude snapshot day), incomplete-history fixed denominator, zero-demand status/coverage, positive-demand coverage, and low-stock cases.
- [x] Keep fixtures small and deterministic; assert exact values and Gold grain/keys.
- [x] Run focused P1-U4 tests and record results: `py -m pytest tests/p1_u4/test_gold.py -q` (1 passed); `py -m pytest tests/p1_u4 -q` (4 passed).
- [x] Run focused tests and record results: `py -m pytest tests/p1_u4/test_gold.py -q` (1 passed); `py -m pytest tests/p1_u4 tests/p2_u1 -q` (4 passed).

### Step 4 — Cube Model and Catalog (P2-US-1; only after Step 1 passes)
- [x] Add version-pinned native Cube project files under `semantic/cube/` using only verified Cube Core packages and the selected local DuckDB driver.
- [x] Declare the DuckDB Python runtime dependency in `pyproject.toml` (the existing P1 code already imports DuckDB but does not declare it).
- [x] Add a small Python bootstrap that creates a local DuckDB catalog file with read-only views over configurable Gold Parquet paths; use it to keep Cube models independent of absolute workspace paths.
- [x] Add local configuration example without secrets; ignore real `.env` files, local DuckDB runtime files, and the disposable spike directory in `.gitignore`.
- [x] Model completed sales, customer, product, and inventory Gold entities with validated keys, joins, descriptions, measures, dimensions, time dimensions, and only documented filter members.
- [x] Model SQL against local Gold Parquet using the proven native DuckDB configuration; do not copy business formulas into a second layer.
- [x] Add a lightweight local validation script or test for model compilation, catalog discovery, and representative metric queries; catalog/query parity check passes.
- [x] Add `tests/p2_u1/test_semantic_views.py` and `scripts/validate_cube_catalog.py` for local catalog setup, model/catalog discovery, and representative metric results; catalog/query parity check passes.

### Step 5 — Handoff Documentation and Review
- [x] Create `aidlc-docs/construction/p2-u1/code/implementation-summary.md` with changed/created paths, semantic names, Gold contract changes, focused commands/results, native runtime evidence, and representative expected results.
- [x] Update the Phase 2 Gold handoff references only where needed; preserve Phase 1 history and make the changed Gold fields explicit.
- [x] Validate no credentials, generated Parquet, local database files, or duplicate/backup code files are tracked.
- [x] Mark each completed step in this plan and prepare P2-U1 review. Do not start P2-U2 until P2-U1 code review and handoff approval.

## Story and Interface Traceability
- **P2-US-1**: Steps 1–5 establish corrected Gold inputs, native Cube feasibility, version-controlled semantic definitions/catalog, representative results, and the U2 handoff.
- **P2-US-2**: Not implemented in this unit; local REST/SQL/MCP interfaces and parity remain P2-U2 after the blocking handoff.
- **Entities owned**: Existing `sales_gold`, `customers_gold`, `products_gold`, and `inventory_gold` outputs; Cube semantic definitions over those files.
- **Expected handoff**: Documented grains/keys/formulas, stable Cube member names, successful native local query proof, representative expected values, and passing focused tests.

## Feasibility Spike Evidence (2026-09-29)
- Node 24.21.0, npm 11.19.0, Python 3.14.4; Python DuckDB 1.5.3.
- Cube Core server and DuckDB driver npm packages: 1.7.47, Apache-2.0. `cubejs-server dev-server` ran directly on Windows without Docker/WSL; the Windows native binding loaded.
- Cube `/v1/meta` returned the Sales catalog. `/v1/load` queried `Sales.netSales` from local `sales_gold.parquet` via DuckDB and returned `345355627.9766`.
- A Python DuckDB 1.5.3 file with Gold Parquet views also queried successfully from Python; Cube's DuckDB Node driver is `@duckdb/node-api` 1.5.5-r.5. Final model path uses a configurable local DuckDB catalog file, subject to runtime verification.
- **Security finding for P2-U2**: Cube 1.7.47 bound API/SQL and Cube Store helper listeners to wildcard addresses during the dev-server test; dev mode disabled authentication. The process was stopped after testing. Do not use dev mode for an ongoing service. P2-U2's NFR design must resolve safe host access/authentication before exposing interfaces; the approved design's loopback-only statement is not met by Cube's default server binding.
- **Configurable Gold access finding**: Cube model JavaScript runs in an isolated schema environment (`process` is undefined). A Python-created local DuckDB catalog with views over configurable Parquet paths is the tested way to keep path configuration out of hard-coded Cube models.

## Plan Approval
**Approved** by the user on 2026-09-29: "approved , do itnow". Execute the numbered steps in order; honor the native-runtime stop condition and P2-U1-to-P2-U2 acceptance gate.
