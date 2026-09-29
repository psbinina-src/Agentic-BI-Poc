# P1-U1 Business Rules — Synthetic Source Contract

## Configuration and Reproducibility
1. Use default seed `42` and inclusive dates `2023-01-01` through `2025-12-31`; seed, dates, customer count, product count, and order-line count are configurable.
2. The default volumes are approximately 10,000 customers, 1,000 products, and exactly 100,000 order lines. Actual order-header count is determined by grouping one or more lines per order.
3. The default date window is fixed, not calculated relative to the runtime clock. Same generator version, effective configuration, and seed must yield the same logical source entities and canonical CSV content.
4. A manifest records effective settings and the resolved window. Runtime-only metadata (for example, generation timestamp) may differ but does not alter the reproducibility comparison of entity data.
5. Reject invalid configuration before publishing source outputs: dates must be valid and ordered, entity volumes positive, and requested date range/volumes supported by generator constraints.

## Synthetic-Only Data
1. All records are generated solely for the PoC; do not read or use production, confidential, or real identifying source data.
2. Customer display names and identifiers are synthetic labels (for example, `Customer 000001`), not realistic or sourced personal identities.
3. Product names, commercial events, payment data, and locations are synthetic categorical values.

## Entity and Relationship Rules
1. Every entity has a unique stable identifier. IDs do not depend on the current time or a nondeterministic random UUID.
2. Each order header references exactly one existing customer and has at least one associated order line.
3. Each order line references exactly one existing order and one existing product. The configured order-line volume is met exactly.
4. Each inventory snapshot references exactly one existing product and has a unique `(snapshot_date, product_id)` key.
5. Source dates fall within the effective inclusive configuration date bounds. Customer acquisition dates cannot be after their first order; product records exist before any line references them.

## Domain Value Rules
1. Quantities are positive integers; unit prices and discount values are nonnegative; line discounts cannot exceed the line's undiscounted value.
2. Order status values are selected from a small documented synthetic domain that includes `completed` and non-completed examples such as `cancelled` or `pending`. Downstream revenue defaults to completed orders; U1 preserves status rather than calculating Gold revenue measures.
3. Customer segment, region, acquisition channel, payment method, product category/subcategory, and product status use documented finite value sets.
4. Inventory on-hand quantity is a nonnegative integer. Reorder points are nonnegative and retained with snapshots so daily stock-risk comparisons are possible.
5. The generator's standard output contains valid business records only. P1-U1 does not generate malformed, duplicate, or referentially invalid rows and does not provide optional negative-data fixtures, per the selected answer. Any negative data-quality tests must be handled outside this unit if required later.

## Analytic Scenario Rules
1. Seeded variation is repeatable and combined with deterministic scenario assignments.
2. At least one defined customer cohort has repeat orders.
3. Sales cover the date window with deterministic time variation and differentiated regional/category allocations suitable for daily/monthly comparisons and downstream forecast evaluation.
4. At least one defined product cohort has recent sales activity and inventory snapshots where on-hand stock is at or below reorder point, allowing low-stock/high-velocity analysis.
5. Scenario checks verify presence, not a production prediction or statistically calibrated distribution. Profile membership and intended behavior are documented.

## Output and Publication Rules
1. Write customer, product, order-header, order-line, and daily inventory-snapshot entities as separate UTF-8 CSV files under the configured source directory.
2. Use documented column names, stable column order, consistent date/numeric formatting, stable row order, and a documented character encoding/delimiter.
3. Publish a manifest only when all expected files are written and source-level validations pass. The manifest includes schema/version, effective seed/window/volumes, counts, paths, checksums, and validation/scenario results.
4. Do not place generated source files or manifests under source control by default; include schemas and instructions, not generated datasets.
5. A same-settings rerun may replace or create outputs only after validating the new set; exact file overwrite/atomic-publication mechanics are finalized during NFR/Code Design.

## Failure Behavior
- Invalid configuration is reported with the specific field/reason and produces no accepted manifest.
- Referential-integrity, required-output, or scenario-presence failures prevent the dataset from being marked successful.
- A failed run reports diagnostics and is not handed to P1-U2 as a valid source contract.
