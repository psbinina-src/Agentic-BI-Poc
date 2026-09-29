# P2-U1 Business Rules — Gold Contract and Semantic Catalog

## Sales and Customers
1. Sales facts contain completed orders only (`order_status = 'Completed'`). Cancelled orders and their lines are excluded from revenue, units, order counts, customer contribution, and repeat-purchase measures.
2. Sales grain is one row per order line. `order_line_id` is unique; order, customer, product, and date keys must resolve to the documented Gold entities.
3. Gross sales is quantity multiplied by unit price. Discount is gross sales multiplied by discount rate. Net sales is gross sales less discount.
4. Order volume is the distinct count of completed `order_id`, not the count of order lines.
5. Customer contribution is completed net sales grouped by customer; any share-of-total is derived from the same completed-order net-sales measure.
6. A repeat customer has more than one distinct completed order. Cancelled orders do not make a customer repeat.

## Inventory
7. Inventory grain is one product-day snapshot. Duplicate `(product_id, snapshot_date)` records fail validation.
8. Sales velocity is completed units sold in the 30 calendar days strictly before the snapshot date divided by 30. Include zero-sale days in the fixed denominator and exclude the snapshot date to prevent look-ahead.
9. If less than 30 days of historical coverage exists, retain the 30-day denominator; unavailable earlier days count as zero demand, as selected by the user.
10. For zero units in the lookback, set velocity to 0, coverage to 0, and coverage status to `no_demand`. Consumers must use the status field to distinguish this sentinel from normal coverage.
11. For positive velocity, stock coverage is on-hand quantity divided by velocity (days). Status is `calculated`.
12. Low-stock is true when inventory on hand is less than or equal to a valid reorder point; otherwise false. Invalid/missing required inventory inputs fail quality validation.

## Semantic and Join Integrity
13. Semantic measures use the corrected Gold contract and have one canonical definition. REST, MCP, or SQL consumers must not redefine metric formulas.
14. Sales and inventory facts are not joined at their raw grains for aggregations. Aggregate each fact independently or use a validated compatible-grain semantic query to prevent duplicated totals.
15. Only documented measures, dimensions, and filters are published in the catalog. P2-U2 enforces its MCP allowlist and rejects arbitrary SQL.
16. Forecast measures remain absent until a forecast Gold dataset is available.

## Quality Gate
P2-U1 passes only if completed-order filtering, grains, key relationships, inventory formulas/status behavior, semantic member metadata, and representative query results are verified and documented. Native Cube Core + DuckDB local feasibility remains a separate exit gate in the implementation/handoff checklist.
