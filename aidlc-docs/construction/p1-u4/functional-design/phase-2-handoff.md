# P1-U4 Phase 2 Handoff Contract

## Phase 2 Gold Contract Update (P2-U1)
- `sales_gold` remains order-line grain and now includes only `Completed` orders; it exposes order `channel` for governed filtering/grouping.
- `inventory_gold` remains product-day grain and exposes `sales_velocity_units_per_day`, `stock_coverage_days`, `stock_coverage_status`, and `low_stock_flag`.
- Velocity is completed-order units over `[snapshot_date - 30 days, snapshot_date) / 30`. Missing earlier days in a partial history window count as zero demand.
- Coverage is on-hand divided by daily velocity for positive demand; zero demand returns coverage `0` with `stock_coverage_status = 'no_demand'`. Positive demand uses status `calculated`.
- The obsolete inventory measure copied from on-hand stock is removed; consumers must use the sales-based velocity field.
- P2-U1 implementation, tests, Cube members, and representative query results are summarized in [the P2-U1 implementation handoff](../../p2-u1/code/implementation-summary.md).

## Required Handoff Artifacts
- Gold fact and dimension tables with documented grain and keys
- Sample query outputs showing sales, customer, and inventory behavior
- A summary of the derived metrics and assumptions
- A clear statement of the final Phase 2 semantic-layer input contract

## Acceptance Criteria
- Sales is at order-line grain.
- Inventory is at product-day snapshot grain.
- Gold tables are derivable from accepted Silver data.
- Business questions for sales, customer repeat behavior, and product inventory risk are demonstrably answerable.
- Local runtime continues to work without container or service dependency.

## Downstream Use
The Gold outputs are the canonical input for the Phase 2 semantic modeling layer and BI activities.
