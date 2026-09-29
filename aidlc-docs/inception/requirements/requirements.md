# Phase 1 Requirements — Lakehouse Foundation and Gold Data Model

## Intent Analysis
- **User request**: Start AI-DLC for Phase 1 and plan stories, units, and slices for one team with one data engineer.
- **Request type**: New implementation phase for the existing Agentic BI PoC requirements.
- **Scope**: Phase 1 only — synthetic source data and Bronze, Silver, and Gold layers.
- **Complexity**: Moderate; includes deterministic data generation, transformations, data quality, dimensional modeling, and reproducible local workflows.
- **Delivery ownership**: One data engineer is accountable for the Phase 1 stories, units, slices, and integration. Sequence dependent work; do not assume parallel developer ownership.

## Source and Decisions
- Governing scope: `requirements/phased/phase-1-lakehouse-gold-data-model.md`.
- Cross-phase context: `requirements/refined_requirement.md` and `requirements/phased/README.md`.
- Implementation choices confirmed during clarification:
  - Python data generator and DuckDB SQL transformations.
  - Synthetic source inputs in CSV; modeled lakehouse outputs in Parquet.
  - Sales fact grain: order line.
  - Inventory grain: daily product-level snapshot.
  - Gold includes a simple deterministic trailing-period baseline forecast for PoC comparison, documented as non-production forecasting.
  - Default generated dataset: three years, approximately 10,000 customers, 1,000 products, and 100,000 order lines; seed, date range, and volume remain configurable.
  - Property-Based Testing extension: disabled.
  - Security Baseline extension: disabled.
  - Resiliency Baseline extension: disabled.

## Functional Requirements

### P1-FR-1: Synthetic Source Generation
1. Provide a Python utility that generates customers, products, orders/order lines, and inventory source records with valid relationships and business-valid values.
2. Support deterministic regeneration from a fixed documented default seed and configurable seed, date range, and entity/order-line volumes.
3. Use CSV for generated raw source files and document schemas, keys, generation settings, and local output paths.
4. Include scenarios supporting daily/monthly sales trends, regional and category comparisons, repeat purchasing, deterministic forecast evaluation, and low-stock/high-velocity inventory analysis.
5. Use only synthetic data; do not use or commit real, confidential, or identifying source data.

### P1-FR-2: Local Lakehouse Layout and Bronze Ingestion
1. Keep implementation and lakehouse artifacts in distinct repository-root areas; organize lakehouse artifacts under a dedicated root `lakehouse/` directory with source-input, Bronze, Silver, and Gold subfolders.
2. Keep generated/runtime data out of version control by default; document output paths and add appropriate ignore rules during implementation.
3. Ingest source CSV files into Bronze with minimal transformation, retain raw values, and capture source, load timestamp, and load status metadata.
4. Make Bronze loads repeatable and traceable to their generated inputs; document reloading and lineage.
5. Do not require Docker, WSL, or a container runtime.

### P1-FR-3: Silver Standardization and Quality
1. Use DuckDB SQL to produce typed, consistently named Silver datasets in Parquet.
2. Validate required fields, data types, business keys, referential integrity, duplicates, and domain constraints before Gold modeling.
3. Document invalid-row, null, duplicate, and correction policies, and make quality outcomes inspectable.
4. Preserve traceability from modeled records to Bronze/source records; support a documented full-refresh workflow and structure transformations for future incremental refresh where appropriate.

### P1-FR-4: Gold Sales and Customer Models
1. Provide a sales fact at order-line grain with stable keys and measures supporting gross revenue, discounts, net revenue, units sold, order-line count, order count, and sales date analysis.
2. Provide conformed date, customer, product, and relevant geography/channel dimensions according to available generated attributes.
3. Support daily/monthly revenue trends, regional/category comparisons, product contribution, growth analysis, order volume, and repeat-purchase analysis.
4. Define customer attributes and activity/profile measures needed for segment, region, acquisition channel, order frequency, lifetime revenue, and last purchase analysis, with derivations documented.
5. Apply the documented default that revenue analyses include completed orders unless a use case explicitly specifies otherwise; define gross and net revenue consistently with the source data contract.

### P1-FR-5: Gold Inventory and Forecast Models
1. Provide daily product-level inventory snapshots with inventory on hand, reorder point, stock status, and the inputs needed for coverage and sales-velocity analysis.
2. Support stock-risk analysis, inventory coverage, product/category demand, and low-stock/high-velocity scenarios.
3. Provide a deterministic, documented trailing-period baseline forecast in Gold for forecast-versus-actual demonstrations. Define the forecast grain, lookback window, date handling, and behavior when insufficient history exists during design; label it as a PoC baseline, not a production forecast.

### P1-FR-6: Delivery and Documentation
1. Document prerequisites, generator configuration and command, source schemas, local layout, layer contracts, transformations, data-quality rules, lineage, and regeneration/reload steps.
2. Provide sample DuckDB queries for sales trends, customer repeat purchases, and inventory risk.
3. Publish stable Gold schemas, grains, keys, metric derivations, and sample outputs for Phase 2 semantic modeling.

## Non-Functional Requirements and Constraints
- **Local-first runtime**: Use native local tools; no container runtime prerequisite. DuckDB operates over local files.
- **Reproducibility**: Same generator version, configuration, and seed must reproduce the same logical dataset.
- **Data privacy**: Synthetic-only source records; no sensitive or production data.
- **Maintainability**: Keep generator, transformation logic, configuration, and lakehouse data concerns separated and inspectable.
- **Testability**: Verify deterministic generation, schema/key integrity, layer quality rules, Gold grains, and sample use cases with repeatable checks. The Property-Based Testing extension is not enabled; focused conventional tests remain required where they validate changed behavior.
- **Scale defaults**: Three years; approximately 10,000 customers, 1,000 products, and 100,000 order lines. Keep each size and date range configurable; inventory snapshot size follows its daily product grain.
- **Storage format**: CSV for raw synthetic inputs; Parquet for Bronze/Silver/Gold lakehouse outputs unless an implementation detail requires retaining a faithful raw CSV copy alongside Bronze tables.
- **Extensions**: Property-Based Testing, Security Baseline, and Resiliency Baseline are disabled for this PoC. Applicable basic data-safety practices remain inherent requirements, including synthetic-only inputs, secret-free source control, and avoiding unnecessary external data sharing.

## Acceptance Criteria
1. The configured generator creates all required synthetic entities with valid keys and relationships, and identical settings/seed reproduce the same logical records.
2. Generated CSV inputs load into Bronze and retain traceable source and ingestion metadata.
3. DuckDB transformations produce typed Silver and documented Parquet Gold outputs in the repository's dedicated `lakehouse/` layout.
4. Quality checks report required-field, type, duplicate, domain, and referential-integrity results and prevent invalid critical records from silently entering Gold.
5. Gold grains and relationships are documented and verified: order-line sales and daily product inventory snapshots.
6. Gold sample queries demonstrate daily/monthly sales trends, customer repeat purchases, and low-stock/high-velocity inventory analysis.
7. The deterministic baseline forecast produces forecast-versus-actual data at its documented grain and handles insufficient history as specified in design.
8. Generation, transformation, and query workflows run locally without Docker, WSL, or container runtime requirements.
9. Gold schemas and sample outputs are ready for Phase 2 semantic modeling.

## Traceability
Detailed source requirements and deliverables remain in [Phase 1 requirements](../../../requirements/phased/phase-1-lakehouse-gold-data-model.md). In particular, this document refines Sections 2.1, 2.2, 4, 5, 7, and 8 using the clarification decisions above. Stories, units, and slices will preserve IDs and acceptance handoffs from that source while adapting the two-developer baseline to one accountable data engineer.
