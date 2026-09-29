# P1-U1 Business Logic Model — Synthetic Source Generation

## Purpose and Boundary
P1-U1 creates reproducible, fully synthetic source entities and publishes CSV inputs plus a manifest in `lakehouse/source/`. It establishes the source contract consumed by P1-U2 Bronze ingestion. It does not load Bronze data or implement Silver/Gold transformations.

## Generation Inputs and Defaults
- **Default seed**: `42`.
- **Default inclusive date window**: `2023-01-01` through `2025-12-31`.
- **Default volume**: approximately 10,000 customers, 1,000 products, and exactly 100,000 order-line records; each setting and date boundary remains configurable.
- **Inventory source grain**: one snapshot per product per calendar day in the configured window. The inclusive 2023-2025 default contains 1,096 calendar days (including leap day 2024); at defaults this is `1,000 × 1,096 = 1,096,000` snapshot rows.
- **Other entities**: order headers are derived from configured order lines by grouping one or more lines per order; header count is therefore a generated result, while line count is the configured target.
- Invalid or incomplete configuration is rejected before source files are published. Required paths, positive entity counts, valid date order, and a usable seed are validated.

## Generation Sequence
1. Resolve and validate the effective configuration and fixed date bounds.
2. Create the product catalog and customer profiles with stable synthetic identifiers.
3. Create order headers and order lines with valid foreign keys, dates, positive quantities, and configured order-line total.
4. Apply deterministic behavior profiles so the fixed dataset contains the required analytic scenarios.
5. Create daily product inventory snapshots, including guaranteed low-stock/high-velocity examples.
6. Check entity counts, unique keys, references, and domain constraints.
7. Write entity CSVs and a manifest with effective configuration, schema/version, counts, output paths, and content checksums.

## Repeatability Model
- For a fixed generator version, seed, date window, and volume/configuration, the same logical entity rows and stable identifiers are produced.
- Stable IDs derive from entity type and deterministic sequence/key, not wall-clock time.
- Seeded variation and scenario assignment use deterministic random state derived from the configured seed. Persist the effective seed/configuration in the manifest.
- Operational manifest fields such as a run timestamp may differ between executions; dataset rows, entity counts, keys, and data-file content are the reproducibility subject. This distinction is documented.
- Output order and CSV serialization are canonicalized (stable row ordering, column ordering, date and numeric formatting) so data files can also be compared consistently.

## Scenario Profiles
The generator combines seeded variation with deterministic scenario rules; it does not rely on chance to produce required examples.
- **Trends and forecast evaluation**: Sales span the full period with repeatable monthly/time variation and enough history for a trailing-period benchmark downstream.
- **Regional/category comparison**: Customer regions and product categories are varied; sales allocation is deterministic and differentiated across these values.
- **Repeat purchasing**: A deterministic subset of customers is assigned multiple orders distributed over the configured window.
- **Inventory risk**: A deterministic subset of products has recent high sales velocity while at least some daily snapshots show on-hand quantity at or below its reorder point.
- The specific profile IDs and qualitative rules are recorded in the manifest/documentation. Exact distribution percentages remain configurable/design details and must not make the named examples disappear.

## Processing Results
The source-generation result contains:
- Paths to customer, product, order, order-line, and inventory-snapshot CSV files.
- Effective seed, fixed/configured date bounds, requested volumes, actual row counts, and schema version.
- Key/referential-integrity validation results and scenario-presence checks.
- Content checksums and a manifest path for downstream ingestion/replay.

## Handoff Boundary
P1-U1 is complete when every expected CSV and manifest field is available, source keys/references and domain rules pass, same-settings regeneration reproduces logical records, and the generation command/result is documented for P1-U2. Bronze conversion, load metadata, and Parquet publication belong to P1-U2.
