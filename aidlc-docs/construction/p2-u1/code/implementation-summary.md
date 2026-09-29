# P2-U1 Implementation Summary — Gold Contract and Semantic Catalog

## Outcome
P2-U1 updates Gold sales/inventory semantics and adds a version-pinned, open-source Cube Core model/catalog over the existing local Parquet files. Forecast measures are not included.

## Gold Contract Changes
- `sales_gold` now includes only completed orders and carries order `channel`.
- Sales remains one row per order line; the existing Gold Parquet filenames are unchanged.
- Inventory remains one product-day row. `sales_velocity_units_per_day` is completed-order quantity over `[snapshot_date - 30 days, snapshot_date) / 30`; same-day sales are excluded and unavailable history days are treated as zero demand per the approved rule.
- `stock_coverage_days` is on-hand divided by daily velocity for positive demand; when demand is zero, coverage is 0 and `stock_coverage_status = 'no_demand'`. Positive-demand rows use `calculated`.
- Low-stock behavior remains `inventory_on_hand <= reorder_point`.

## Semantic Catalog
Cube Core 1.7.47 (Apache-2.0) defines four cubes: `Sales`, `Customers`, `Products`, and `Inventory`. Measures include gross sales, discount, net sales, units sold, order-line count, distinct completed order count, customer contribution share, inventory on hand, low-stock rows, average daily sales velocity, and average product-day coverage. A hidden multi-stage grand-total measure supports customer contribution share. Sales/customer/product/inventory joins use the documented keys and facts retain their own grains.

## Local Runtime Proof
- Node 24.21.0, npm 11.19.0, Python 3.14.4, Python DuckDB 1.5.3; Cube DuckDB Node driver uses `@duckdb/node-api` 1.5.5-r.5.
- Native Cube Core server and DuckDB driver 1.7.47 ran on Windows without Docker or WSL.
- `prepare_gold_views.py` created an ignored local DuckDB catalog with views over each Gold Parquet file using a configurable Gold path.
- `py semantic/cube/prepare_gold_views.py` created an ignored local DuckDB catalog with views over each Gold Parquet file using a configurable Gold path. The catalog bootstrap test covers paths containing spaces and apostrophes.
- Authenticated production-mode REST validation compiled the four cubes and returned Sales, Customer-region, customer-contribution-share, and Inventory metrics. `py scripts/validate_cube_catalog.py` compared the results against independent DuckDB scans of Gold Parquet and passed.
- Representative completed sales query results: total net sales **310,698,017.5764** and **44,991** distinct completed orders. By channel: Retail **104,015,530.7891**, Marketplace **103,577,839.5719**, Online **103,104,647.2154**; **14,997** completed orders per channel.
- Tests: `py -m pytest tests/p1_u4 -q` — **4 passed**. `py -m compileall -q src/p1_u4 semantic/cube/prepare_gold_views.py scripts/validate_cube_catalog.py` passed.
2. From the repository root, run `py semantic/cube/prepare_gold_views.py`; it writes `.local/agentic_bi.duckdb` with views over the Gold Parquet files. The catalog bootstrap test covers paths containing spaces and apostrophes. Stop Cube before rebuilding this catalog because DuckDB locks an open database file.
- Tests: `py -m pytest tests/p1_u4 tests/p2_u1 -q` — **4 passed**. `py -m compileall -q src/p1_u4 semantic/cube/prepare_gold_views.py scripts/validate_cube_catalog.py` passed.

## Local Setup (P2-U1)
1. Run the existing Gold build with the intended Silver/Gold paths.
2. From the repository root, run `py semantic/cube/prepare_gold_views.py`; it writes `.local/agentic_bi.duckdb` with views over the Gold Parquet files. Stop Cube before rebuilding this catalog because DuckDB locks an open database file.
3. In `semantic/cube/`, run `npm install`, copy `.env.example` to an untracked `.env`, and replace the API secret with a local random value. Keep `CUBEJS_DEV_MODE=false`.
4. Run `npm start` from `semantic/cube/`. REST metadata and load APIs are served on the configured port (default 4000). SQL API is not enabled by P2-U1; SQL configuration belongs to P2-U2.
5. Supply a locally generated JWT as `CUBE_API_TOKEN` and run `py scripts/validate_cube_catalog.py` from the repository root. The script checks metadata and compares governed results with DuckDB scans over Gold.

## Security / P2-U2 Gate
The Cube 1.7.47 server test binds the API to wildcard addresses even when queried at `127.0.0.1`; the documented server configuration inspected here exposes no host-bind option. Development mode also disables authentication and is **not** suitable as the running setup. The recorded parity run used `CUBEJS_DEV_MODE=false` with a local JWT. P2-U2 must resolve the approved design's loopback-only constraint and SQL API authentication before exposing the service/interfaces; do not use development mode, add a hosted service, or introduce a container runtime as an implicit workaround.

## Handoff to P2-U2
- Stable Cube model members and four-cube catalog are version controlled under `semantic/cube/model/`.
- Corrected Gold grains, field names, and measures are documented in the P2-U1 Functional Design.
- Native startup and representative governed REST queries have been demonstrated against Gold.
- `py scripts/validate_cube_catalog.py` is the repeatable expected-result/parity baseline for REST versus DuckDB. P2-U2 adds SQL/MCP interface checks after resolving local service access controls.
