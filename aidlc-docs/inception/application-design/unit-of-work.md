# Phase 1 Units of Work

## Delivery and Organization Baseline
- **Team/owner**: One team; one data engineer is accountable for all units, slices, tests, and integration.
- **Execution**: Strictly sequential P1-U1 -> P1-U2 -> P1-U3 -> P1-U4. A dependent unit does not start until the prior unit's contract and acceptance checks pass.
- **Unit meaning**: Logical development grouping in one modular Python application, not separately deployable services.
- **Code organization (greenfield)**: Python modules and SQL under `src/`; tests under `tests/`; generated/runtime data under `lakehouse/source/`, `lakehouse/bronze/`, `lakehouse/silver/`, and `lakehouse/gold/`. Keep runtime datasets out of source control by default.
- **Data contracts**: CSV source inputs and Parquet layer outputs with documented paths, keys/schema, and lineage.
- **Evidence standard**: Each unit publishes a concise checklist of outputs, contract/quality checks, and a representative command or result. Exact automated test design is finalized in Construction.

## P1-U1 — Synthetic Generator and Source Contract
- **Story**: P1-US-1.
- **Accountable owner**: Data engineer.
- **Purpose**: Establish deterministic source data and the contract consumed by Bronze ingestion.
- **Responsibilities/deliverables**:
  - Configurable synthetic customer, product, order/order-line, and inventory generation.
  - Fixed documented default seed; configurable seed, date range, and data sizes.
  - CSV entity files and a generation manifest in `lakehouse/source/`.
  - Source schema/key documentation and generation instructions.
- **Implementation slices (sequential)**:
  1. Define source entities, keys, required attributes, and generator configuration.
  2. Implement deterministic generation and reproducibility check.
  3. Write CSV files/manifest and validate referential integrity/business-valid scenarios.
  4. Document regeneration command, defaults, configurable options, and sample outputs.
- **Acceptance/handoff checklist**:
  - Required synthetic entities and documented keys/schemas are present.
  - Same generator version/configuration/seed reproduces the same logical dataset.
  - Default size/date settings and output paths are recorded; generated files are not committed by default.
  - Sample command/output and source manifest are published for U2.
- **Representative evidence**: Generator run summary with configuration, seed, entity counts, file paths, and successful key-integrity/reproducibility result.
- **Predecessor**: None.
- **Exit handoff to P1-U2**: Stable CSV schemas, keys, manifest fields, configuration defaults, sample files, and reproducible generation result.

## P1-U2 — Bronze Ingestion and Lineage
- **Story**: P1-US-1.
- **Accountable owner**: Data engineer.
- **Purpose**: Load generated source files repeatably into the raw-preserving Bronze layer.
- **Responsibilities/deliverables**:
  - Stage-specific local ingestion operation using DuckDB.
  - Bronze Parquet outputs in `lakehouse/bronze/`, retaining raw business values.
  - Source, load timestamp, load status, and traceability metadata.
  - Reload/run instructions and source-to-Bronze lineage.
- **Implementation slices (sequential)**:
  1. Consume and validate the accepted P1-U1 manifest and CSV contract.
  2. Implement CSV-to-Parquet ingestion and load metadata capture.
  3. Verify entity counts, required keys, raw-value retention, and repeatable reload behavior.
  4. Publish Bronze paths/schema and a sample ingestion report.
- **Acceptance/handoff checklist**:
  - Each agreed source entity loads to its documented Bronze Parquet output.
  - Raw business values and the expected key relationships remain traceable.
  - Load metadata and status are available; missing/invalid input is surfaced rather than silently accepted.
  - Representative ingestion command/result and reload instructions are documented.
- **Representative evidence**: Ingestion summary showing source and output paths, row counts, metadata/status, and check results.
- **Predecessor**: P1-U1; do not begin contract-dependent ingestion acceptance until U1 handoff passes.
- **Exit handoff to P1-U3**: Verified Bronze schemas/keys, file paths, metadata, row counts, and successful load evidence.

## P1-U3 — Silver Standardization and Data Quality
- **Story**: P1-US-2.
- **Accountable owner**: Data engineer.
- **Purpose**: Produce consistent, typed Silver data and inspectable quality outcomes from the accepted Bronze contract.
- **Responsibilities/deliverables**:
  - DuckDB SQL transformations under `src/` and Parquet outputs in `lakehouse/silver/`.
  - Documented required-field, type, null/invalid-row, duplicate-key, domain, and referential-integrity policies.
  - Quality reports and lineage back to Bronze/source records.
  - Repeatable full-refresh workflow; transformation organization suitable for future incremental processing.
- **Implementation slices (sequential)**:
  1. Map Bronze schemas to standardized Silver names/types and record lineage.
  2. Implement Silver transformations and configured row handling.
  3. Implement and run quality checks; make critical failures inspectable and blocking before Gold.
  4. Verify full refresh, output contracts, and report/sample query evidence.
- **Acceptance/handoff checklist**:
  - Each agreed Bronze input has a typed Silver output with documented schema and lineage.
  - Data-quality policies and outcomes for required values, types, duplicates, domain rules, and relationships are documented.
  - Critical failed checks do not pass silently into Gold.
  - Representative transformation/validation command and report are provided.
- **Representative evidence**: Silver schema/row summary and a quality report with named check outcomes.
- **Predecessor**: P1-U2; stop if Bronze schemas, keys, or load evidence fail the handoff.
- **Exit handoff to P1-U4**: Accepted Silver schema, keys, lineage, quality policies/results, output paths, and completed checks.

## P1-U4 — Gold Dimensional Models, Samples, and Phase 2 Handoff
- **Story**: P1-US-2.
- **Accountable owner**: Data engineer.
- **Purpose**: Publish the business-ready dimensional model as the BI foundation and stable input contract for Phase 2.
- **Responsibilities/deliverables**:
  - Gold sales fact at order-line grain and appropriate date/customer/product/geography/channel dimensions.
  - Customer profile/activity outputs and product/inventory fact at daily product-snapshot grain.
  - Documented measures, including the deterministic trailing-period forecast baseline and its limitations.
  - Sample DuckDB queries for sales trends, repeat purchasing, and inventory risk.
  - Gold schema, keys, grains, derivations, lineage, sample outputs, and Phase 2 handoff documentation.
- **Implementation slices (sequential)**:
  1. Define and publish the Gold dimensional grain, keys, conformed dimensions, and measure contract from accepted Silver inputs.
  2. Implement sales and customer models and check order-line grain/revenue behavior.
  3. Implement inventory snapshot, stock health/velocity, and forecast baseline outputs.
  4. Run quality checks and sample business queries; document schemas, derivations, outputs, and downstream usage.
- **Acceptance/handoff checklist**:
  - Sales is at order-line grain; inventory is at daily product-level snapshot grain.
  - Gold supports sales, customer repeat-purchase/profile, and low-stock/high-velocity inventory questions.
  - Revenue uses the documented completed-order default; forecast grain/window/insufficient-history handling and non-production status are documented.
  - Gold outputs, sample queries, paths, keys, measures, lineage, and quality evidence are published for Phase 2 semantic modeling.
  - Integrated generation-to-Gold run succeeds locally without a container runtime.
- **Representative evidence**: End-to-end run summary, Gold schema/model contract, quality report, and sample query outputs for all three use cases.
- **Predecessor**: P1-U3; stop if Silver output contract or quality gate fails.
- **Phase exit handoff**: Stable Gold dimensional contract and evidence accepted for Phase 2.

## Phase-Level Acceptance
- Complete U1 -> U2 -> U3 -> U4 in sequence under the single data-engineer owner.
- Each unit's documented handoff is accepted before dependent work begins.
- Phase exit requires the end-to-end generator-to-Gold flow, quality evidence, sample analyses, reproducibility, and Gold contract publication.
