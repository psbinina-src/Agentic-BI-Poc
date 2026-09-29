# Phase 2 Summary — Local Gold REST API

## Purpose
Phase 2 exposes the Phase 1 Gold Parquet datasets through a small local REST API for Phase 3 Agentic BI. The API provides dataset discovery, field metadata, and bounded read-only query access. It does not add a semantic layer or redefine business metrics.

## Current Delivery Status (2026-09-30)
- **P2-U1 — Gold contract and Cube catalogue prototype: existing work retained as optional reference.** Cube is not required by the Phase 2 REST API or Phase 3 runtime path.
- **P2-U2 — Local Gold REST API: complete.** Catalogue, schema, relationship, bounded-query endpoints, tests, and local usage instructions are verified.
- **Phase acceptance: complete; Phase 2 is closed.** Full project tests, Gold validation, dependency/compile checks, and the live REST smoke test passed.

## Phase 1 Gold Inputs and P2-U1 Contract
Gold Parquet files remain in `lakehouse/gold/`:
- `sales_gold.parquet`: one completed-order line per row; carries order channel, customer, product, and order date. Cancelled-order lines are excluded.
- `customers_gold.parquet`: one row per customer.
- `products_gold.parquet`: one row per product.
- `inventory_gold.parquet`: one product-day snapshot per row, with inventory, reorder point, low-stock flag, sales velocity, coverage, and coverage status.

Inventory velocity uses completed units in the 30 full calendar days strictly before the snapshot, divided by 30. The snapshot date is excluded; missing earlier history days count as zero demand. For positive velocity, coverage is on hand divided by velocity and status is `calculated`. For zero demand, velocity and coverage are 0 and status is `no_demand`.

Forecast measures remain out of scope until a forecast Gold dataset exists.

## REST API Contract
- `GET /health`: API and Gold dataset availability.
- `GET /catalog`: four Gold dataset names, descriptions, grains, key fields, availability, and approved relationships (sales-to-customer/product; inventory-to-product).
- `GET /catalog/{dataset}`: field names/types discovered from Parquet, with concise field descriptions.
- `POST /query`: validated field projection/filtering, optional approved dimension joins, grouping and generic aggregates, order, and bounded results.
- Query access is limited to `sales_gold`, `customers_gold`, `products_gold`, and `inventory_gold`; only documented joins are allowed; default limit 100, hard maximum 500.
- The API exposes Gold fields and generic aggregates, not centrally governed business metrics. Phase 3 interprets the metadata and selects queries.

## Runtime and Security Notes
- Native Python FastAPI/Uvicorn and embedded DuckDB read local Gold Parquet; no Docker, WSL, Node, Cube, or external database is needed for this API.
- The documented server binds to `127.0.0.1` only. It has no remote authentication because remote access is explicitly out of scope; do not bind to wildcard addresses or expose the port.
- Only fixed Gold dataset files and schema-validated fields are queryable. Filter values are parameterized; arbitrary SQL and client-supplied paths are rejected.
- Stop the server after local testing. No secrets or copied database are required.

## Start and Test Commands
Run these commands from the repository root in PowerShell.

Install the API and test dependencies:

```powershell
py -m pip install -e ".[test]"
```

Start the API in its own terminal. Keep the loopback bind; stop it with `Ctrl+C` when finished:

```powershell
py -m uvicorn p2_u2.api:app --app-dir src --host 127.0.0.1 --port 8100
```

With the API running, smoke-test health, catalogue, and sales schema discovery:

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8100/health'
Invoke-RestMethod -Uri 'http://127.0.0.1:8100/catalog'
Invoke-RestMethod -Uri 'http://127.0.0.1:8100/catalog/sales_gold'
```

Run focused or full automated tests from another terminal:

```powershell
py -m pytest tests/p2_u2 -q
py -m pytest -q
```

## Validation Evidence
- REST API tests: `py -m pytest tests/p2_u2 -q` — **7 passed**.
- Full project tests: `py -m pytest -q` — **20 passed**.
- `py -m compileall -q src/p2_u2 tests/p2_u2` and `py -m pip check` — passed.
- Live loopback smoke check: all four Gold datasets were available; catalogue and dataset details returned HTTP 200; sales-by-customer-region join returned five regional groups. Server was stopped after verification.
- P2-U1 historical implementation details: [P2-U1 implementation handoff](../construction/p2-u1/code/implementation-summary.md).

## Phase 3 Handoff
Phase 3 should call this local REST API for catalogue discovery and Gold data access. It should not read Parquet directly or depend on Cube/MCP. Keep API results bounded and pass only the minimum context needed to any model.
