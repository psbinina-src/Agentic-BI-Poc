# P2-U2 Code Generation Plan — Local Gold REST API

## Unit Context
- **Story**: P2-US-2 — the Phase 3 agent can discover and retrieve bounded data from the Gold model.
- **Dependencies**: Phase 1 Gold Parquet contract and approved P2-U2 functional/NFR designs.
- **Owner**: One data engineer; implement and verify sequentially.
- **Runtime**: Python FastAPI with DuckDB scanning the existing Gold Parquet files; bind only to `127.0.0.1`.
- **Scope boundary**: No Cube calls, MCP, SQL text endpoint, business semantic layer, BI protocol, remote auth, or hosted runtime.

## Numbered Generation Steps

### Step 1 — Gold Catalogue and Schema Discovery
- [x] Define the four allowed Gold datasets, descriptions, grains, key fields, and fixed fact-to-dimension relationships.
- [x] Discover physical field names and DuckDB types from each available Parquet schema; attach concise field descriptions.
- [x] Expose `GET /health`, `GET /catalog`, and `GET /catalog/{dataset}`.
- [x] Test catalogue content, physical field metadata, and unavailable/unknown datasets.

### Step 2 — Bounded Read-Only Data Access
- [x] Add `POST /query` with allowlisted dataset names, approved dimension joins, selected fields, parameterized filters, optional grouping, generic field aggregations, ordering, and limit.
- [x] Validate identifiers against the selected physical Gold schema; reject arbitrary SQL and unknown members.
- [x] Apply a default row limit of 100 and hard maximum of 500; serialize date and decimal values as JSON values.
- [x] Test filtered data, grouped aggregates, bounds, malformed/unsafe input, and unknown fields/datasets.

### Step 3 — Local Run Contract and Phase 3 Handoff
- [x] Document install/start commands, endpoint examples, response shape, Gold path override, and loopback-only runtime.
- [x] Explain the API exposes raw fields and generic aggregates, not governed business metrics; Phase 3 owns interpretation.
- [x] Record changed files, verification results, and known limitations in the P2-U2 implementation summary.

### Step 4 — Final Verification
- [x] Run focused P2-U2 tests and the complete existing test suite.
- [x] Run a local HTTP smoke test against the actual Gold Parquet files, then stop the server.
- [x] Confirm no SQL execution endpoint, remote bind, credential, generated data, or new semantic definitions were introduced.
- [x] Update this plan and the Phase 2 state immediately after each completed step.

## Story Traceability
- **P2-US-1**: Dataset catalogue and schema endpoints expose names, descriptions, grains, keys, field names, types, and descriptions.
- **P2-US-2**: The constrained query endpoint supplies Phase 3 with bounded local Gold data.
- **Gold contract**: `sales_gold`, `customers_gold`, `products_gold`, and `inventory_gold` only; no competing metric formulas are created.

## Code Locations
- `src/p2_u2/api.py`
- `src/p2_u2/gold_access.py`
- `tests/p2_u2/test_api.py`
- `pyproject.toml`
- `aidlc-docs/phase-2/phase-2-commands.md`
- `aidlc-docs/phase-2/phase-2-summary.md`
- `aidlc-docs/construction/p2-u2/code/implementation-summary.md`

## Approval and Progress
User approved the REST-over-Gold direction with the request: "ok letsdo that for phase2 then, endpoint would expose data catagloue/datasets/field details and also the data model/data access for phase 3 agentic BI". The local Gold REST API and focused tests are implemented; Steps 1 and 2 are complete. Continue with documentation and final verification.
