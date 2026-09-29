# Phase 1 User Stories — Lakehouse Foundation and Gold Data Model

## Delivery Baseline
- **Team**: One team with one data engineer.
- **Accountable owner**: The data engineer owns both stories and all related units/slices, in sequence. Story boundaries do not imply parallel delivery.
- **Story organization**: Two outcome-led stories, using the source Phase 1 IDs; Bronze/source foundation first, followed by Silver/Gold analytics outcomes.
- **Acceptance style**: Concise, observable input/output/criteria. Detailed technical checks and precise thresholds are to be defined in design and tests, not expanded into extra stories.

## P1-US-1: Reproducible Synthetic Data and Bronze Inputs

**Story**  
As a data engineer, I want to reproducibly generate synthetic e-commerce source data and load it into Bronze, so that downstream transformations have stable, traceable inputs.

**Owner**: Data engineer (single accountable owner)

**Scope**: Configurable deterministic generator for customer, product, order/order-line, and inventory records; documented CSV source contract; local Bronze ingestion and metadata. Default settings are three years, approximately 10,000 customers, 1,000 products, 100,000 order lines, and a fixed documented seed. The repository-root lakehouse layout separates source inputs and Bronze from application/transformation code.

**Acceptance criteria**
1. Given the same generator version, configuration, and seed, regeneration produces the same logical entity records and relationships.
2. The default and configurable generator produce synthetic customers, products, orders/order lines, and inventory with valid keys and business-valid relationships over the configured date range.
3. Generated raw source files are CSV, their schemas/configuration/output location are documented, and generated runtime data is excluded from source control by default.
4. Source inputs can be ingested locally into the documented Bronze location as Parquet while retaining raw business values and recording source/load metadata and status.
5. The generation and Bronze-load workflow runs without Docker, WSL, or another container runtime, and the source/Bronze contract is documented for the next slice.

**Requirement traceability**: P1-FR-1, P1-FR-1A, P1-FR-2; approved Phase 1 requirements P1-FR-1 and P1-FR-2; source story P1-US-1.

**Handoff to P1-US-2**: Publish entity schemas, primary/business keys, seed and configuration defaults, representative samples, source/Bronze paths, metadata fields, and a successful repeatable load result. The same data engineer consumes this contract before finalizing Silver mappings.

## P1-US-2: Trusted Gold Models for Analytics

**Story**  
As an analytics consumer, I want clean, documented Gold models for sales, customer, and inventory analysis, so that I can answer the Phase 1 business questions with consistent data.

**Owner**: Data engineer (single accountable owner); analytics consumer is the beneficiary/persona.

**Dependency**: P1-US-1 source and Bronze contract is stable and validated. Work is sequenced by the same data engineer; this is a logical dependency, not a developer-to-developer transfer.

**Scope**: DuckDB SQL transformations from Bronze through typed, quality-checked Silver to documented Parquet Gold; sales at order-line grain, daily product inventory snapshots, customer activity/profile attributes, and a deterministic baseline forecast. Keep transformations, tests, documentation, and lakehouse data in clearly separated repository-root areas.

**Acceptance criteria**
1. Bronze inputs are standardized into Silver with documented types and policies for required fields, invalid/null values, duplicate business keys, domain constraints, and referential integrity; quality outcomes are inspectable.
2. Gold sales data is at order-line grain and supports documented gross/net revenue, discounts, units, order counts, date trends, regional/category/product comparisons, and repeat-purchase analysis. Revenue defaults to completed orders.
3. Gold customer and product/inventory models expose the documented profile, segment, region, product/category, daily on-hand, reorder, coverage/velocity, and status attributes needed for customer and stock-risk analysis.
4. A deterministic trailing-period baseline forecast supports forecast-versus-actual analysis; its grain, lookback, and insufficient-history behavior are documented, and it is identified as a PoC baseline rather than a production forecast.
5. Sample DuckDB queries demonstrate sales trends, customer repeat purchasing, and low-stock/high-velocity inventory scenarios using the Gold outputs.
6. Gold schemas, keys, grains, measure derivations, lineage, sample outputs, local paths, and refresh/regeneration instructions are documented and suitable for Phase 2 semantic modeling.
7. The integrated generator-to-Gold flow runs locally without a container runtime and satisfies the Phase 1 acceptance outcomes.

**Requirement traceability**: P1-FR-2 through P1-FR-6; approved Phase 1 requirements P1-FR-3 through P1-FR-6; source story P1-US-2.

**Phase integration gate**: The data engineer verifies the generated source/Bronze contract is consumed by Silver/Gold, reconciles schema or data-quality mismatches, runs end-to-end checks and sample queries, and publishes the final Gold contract and evidence before Phase 1 is accepted.

## Story Quality and Coverage
- Stories preserve the two Phase 1 source outcomes and are sized as broad, independently verifiable business outcomes; implementation details are sequenced later as units and slices.
- Acceptance criteria are observable and cover the agreed input/output/outcome level. Numeric quality thresholds and forecast formula specifics remain design decisions, not assumptions in these stories.
- Both stories have one accountable owner, explicit dependencies/handoff, and testable outcomes.
- Together, the stories cover synthetic generation, Bronze ingestion, Silver quality, Gold sales/customer/inventory, forecast demonstration, sample queries, lineage, reproducibility, and the Phase 2 Gold contract.
