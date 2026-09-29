# Phase 1: Lakehouse Foundation and Gold Data Model

## 1. Objective

Establish the lakehouse data foundation required to support the Agentic BI and dashboarding use cases. This phase covers the ingestion and transformation flow from raw source data into a governed analytical model optimized for business intelligence consumption.

## 2. Scope

This phase shall implement the lakehouse progression:

- Bronze layer: raw source data as-is
- Silver layer: cleansed, standardized, and quality-checked data
- Gold layer: business-ready dimensional and fact models for BI use cases

### Local Runtime

1. Store Bronze, Silver, and Gold artifacts on local storage for the PoC; this phase does not require Docker, WSL, or a container runtime.
2. Document the chosen ingestion and transformation tools when they are selected. This phase does not prescribe a container or a specific ETL runtime.

The Gold layer shall be modeled to support the requested BI functions:

- sales monitoring and forecasting
- customer profile review
- product inventory management

## 2.1 Development Data Provisioning

1. Phase 1 shall provide a reproducible synthetic e-commerce dataset for development, testing, and demonstration; external or production data is not required.
2. Synthetic records shall contain no real personal, confidential, or production data.
3. The dataset shall cover customers, products, orders and sales transactions, and inventory snapshots or movements, with valid keys and relationships between entities.
4. Data shall span a documented configurable time period and include enough history and variation to demonstrate daily/monthly trends, regional and category comparisons, repeat purchasing, forecasting-style analysis, and low-stock/high-velocity inventory scenarios.
5. Provide a data-generation utility and configuration, including a fixed default random seed, so the same settings reproduce the same logical dataset. Allow the dataset size and date range to be changed for development and performance testing.
6. Generated source data shall be available locally as Bronze-layer inputs. Document the schema, generation command, configuration, output location, and how to regenerate the data; do not require generated data files to be committed to source control.
7. The data-generation approach and file format shall be compatible with the selected local ingestion/transformation workflow and DuckDB access. The generator implementation technology may be selected during Phase 1 design.

## 2.2 Two-Developer Stories, Units, and Handoffs

| Story | User story outcome | Unit(s) | Owner | Dependency / acceptance handoff |
|---|---|---|---|---|
| P1-US-1 | As a developer, I can reproducibly generate and ingest synthetic source data so downstream models have stable inputs. | P1-U1: generator, deterministic configuration, and source schema; P1-U2: Bronze ingestion, metadata, and lineage | Developer A | Publish entity schemas, keys, seed/configuration, sample files, and Bronze locations. Verify regeneration with the same configuration and successful Bronze load. |
| P1-US-2 | As an analytics consumer, I can use clean, documented Gold models for sales, customer, and inventory analysis. | P1-U3: Silver standardization and data-quality rules; P1-U4: Gold facts/dimensions, lineage, and sample queries | Developer B | Agree source/Bronze contract with Developer A before transformation work. Verify Gold grain, key relationships, required measures/dimensions, quality checks, and sample use-case queries; publish the Gold schema and examples for Phase 2. |

**Integration gate:** Developer A hands off the source and Bronze contract before Developer B finalizes Silver/Gold mappings. Both owners run the agreed end-to-end data flow together and resolve schema or data-quality mismatches before Phase 1 is accepted.

## 3. Architecture Overview

### Bronze Layer

The bronze layer represents raw operational data as loaded from source systems, without major transformation.

Requirements:

- preserve source fidelity and lineage
- store raw files or raw tables in near-original format
- keep immutable source snapshots where possible
- support auditability and reloading

Expected characteristics:

- original column names and source values retained
- minimal cleaning or type conversion
- ingestion tracking for load timestamps and source metadata
- support for multiple source feeds if required

### Silver Layer

The silver layer represents standardized, cleaned, and enriched data ready for downstream analytics.

Requirements:

- apply data quality checks
- standardize naming conventions
- convert data types into analytics-friendly formats
- clean invalid or incomplete records
- enrich with derived fields when needed
- support incremental and latest-state processing

Examples of silver-level transformations:

- date normalization
- null handling and defaulting
- duplicate removal
- standardizing product, customer, and region values
- converting string identifiers to canonical values
- adding load date, effective date, or record status fields

### Gold Layer

The gold layer shall represent the business-ready analytical model used for BI reporting and AI query resolution.

Requirements:

- model dimensions and fact tables required by the business use cases
- align with analytics semantics for sales, customer, and inventory analysis
- support dashboard and GenAI-driven question answering
- provide stable business definitions for downstream consumption

## 4. Functional Requirements

### P1-FR-1: Bronze Layer Ingestion

1. The system shall ingest source data into the bronze layer with minimal transformation.
2. The bronze layer shall retain raw values for traceability and reprocessing.
3. The system shall capture ingestion metadata such as source, timestamp, and load status.
4. Bronze data shall be retained as the trusted raw source for future regeneration.

### P1-FR-1A: Synthetic Development Data

1. The system shall include a utility to generate the synthetic e-commerce source data described in Section 2.1.
2. The generator shall produce records for sales, customers, products, and inventory with referential integrity and business-valid values suitable for the Phase 1 models.
3. The generator shall support deterministic regeneration using a documented seed and configurable data volume and date range.
4. The generated data shall include scenarios that exercise the required analytics, including sales trends, customer repeat purchases, and inventory risk; the scenarios and any assumptions shall be documented.
5. Generated files shall be written to a documented local input location and be consumable by the Bronze ingestion process.

### P1-FR-2: Silver Layer Standardization

1. The system shall cleanse and standardize source data in the silver layer.
2. The system shall convert raw data types into analytical-ready formats.
3. The system shall handle invalid rows according to configured rules.
4. The system shall support latest-state processing and incremental refresh logic when needed.
5. The system shall apply standard enrichment such as date dimensions, normalized categories, and business keys.

### P1-FR-3: Gold Layer Business Modeling

1. The gold layer shall include fact tables supporting sales monitoring and forecasting.
2. The gold layer shall include customer dimension tables and customer activity profiles.
3. The gold layer shall include product and inventory fact/dimension structures supporting stock analysis.
4. The gold layer shall model measures such as revenue, units sold, order count, forecast amount, and inventory status.
5. The gold layer shall provide a business-friendly shape optimized for BI reports and AI semantic resolution.

### P1-FR-4: Sales Monitoring Data Model

The sales model shall support:

- monthly and daily revenue trends
- region and category performance
- sales growth analysis
- product contribution analysis
- order count and unit sales tracking
- forecast vs actual comparisons

Required measures may include:

- gross revenue
- net revenue
- units sold
- discount amount
- order count
- growth rate
- forecasted revenue

### P1-FR-5: Customer Profile Data Model

The customer model shall support:

- customer segmentation
- customer contribution by region and segment
- repeat purchase behavior
- customer value analysis
- profile-based filtering for business questions

Required attributes may include:

- customer_id
- customer_name
- customer_segment
- region
- acquisition channel
- order frequency
- lifetime revenue
- last purchase date

### P1-FR-6: Product and Inventory Data Model

The product inventory model shall support:

- product and category performance
- stock availability and stock coverage
- inventory aging and health
- product contribution to revenue
- sales velocity and low-stock risk review

Required attributes may include:

- product_id
- product_name
- category
- subcategory
- inventory_on_hand
- reorder_point
- stock_coverage_days
- sales_velocity
- inventory_status

## 5. Data Quality Rules

1. The system shall validate required fields before loading to the silver or gold layer.
2. Null and malformed values shall be handled according to a documented policy.
3. Duplicate records shall be identified and resolved using business keys.
4. Data type mismatches shall be corrected before gold-layer modeling.
5. Critical business facts shall be traceable back to source records.

## 6. Gold Layer Output Expectations

The gold layer shall be ready for:

- semantic layer modeling
- metric definition in Cube or equivalent semantic stack
- dashboard consumption
- AI natural-language query mapping
- traditional BI validation

## 7. Acceptance Criteria

The phase is complete when:

1. bronze data is ingested and retained in raw form
2. silver data is cleaned and standardized with validated types
3. gold data is modeled for sales, customer, and inventory analytics
4. the data model is compatible with downstream semantic modeling
5. the gold layer supports the planned BI and Agentic BI use cases
6. the Gold-layer outputs are available at a documented local path for the downstream semantic layer
7. the synthetic dataset generator produces all required source entities and can recreate the same logical dataset with the same configuration and seed
8. generated data loads through Bronze, Silver, and Gold and supports sample queries for sales trends, customer repeat-purchase analysis, and inventory risk

## 8. Deliverables

- synthetic e-commerce data generator, configuration, and reproducibility instructions
- documented synthetic source schemas and local data-generation/output locations
- bronze raw ingestion artifacts
- silver transformation logic and data quality rules
- gold fact and dimension model definitions
- documented data lineage and transformation mapping
- data validation checks and sample reports
