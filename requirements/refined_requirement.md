# Refined Requirement: Agentic BI Proof of Concept

## 1. Purpose

This project defines a rapid end-to-end Agentic BI proof of concept using open-source application components to enable natural-language analytics over a local lakehouse, while preserving metric governance and traditional BI validation. The PoC runs application components natively on the local host without Docker; it uses the external OpenAI API for language-model capabilities.

The solution must demonstrate that a user can ask a business question in plain English, have an AI agent resolve the correct semantic model, execute a governed query, and render an analytical visualization without custom chart code.

## 2. Product Goal

Build a local-first, open-source Agentic BI workflow that allows users to:

- ask business questions in natural language
- resolve those questions to verified semantic metrics and dimensions
- query a governed analytics layer using DuckDB and Cube Core
- generate and render valid Vega-Lite chart specifications
- validate results against a traditional BI view using Metabase

The project is intended as a PoC for demonstrating single-source metric truth across AI-driven and conventional BI workflows.

## 3. Scope

### In Scope

- local lakehouse-style analytics storage using DuckDB
- semantic metric governance using Cube Core
- natural-language catalog resolution and metric mapping
- ReAct-style orchestration using LangGraph
- chart generation through Vega-Lite JSON specs
- interactive dashboard rendering with Next.js
- traditional BI comparison via Metabase
- local deployment without Docker or another container runtime; application services run as native host processes with documented setup and startup steps

### Out of Scope

- cloud-only data warehouse dependencies
- hardcoded chart component logic for each chart type
- custom BI authoring experience beyond PoC validation
- production-grade enterprise governance beyond PoC requirements
- large-scale multi-tenant deployment
- container-based packaging as a prerequisite for the PoC

## 4. Business Context

Organizations increasingly want business users to query data using natural language without sacrificing trust, consistency, or metric governance. This PoC addresses that gap by combining:

- a governed semantic layer for metric definitions
- an AI agent for business question interpretation
- a visualization engine for chart synthesis
- traditional BI validation to confirm parity of results

## 5. Architectural Overview

The target architecture is a layered, local-first system built primarily from open-source components. The OpenAI API is an external, hosted LLM dependency:

| Layer | Technology | Purpose |
|---|---|---|
| Storage and query engine | DuckDB | Query local analytical data files |
| Semantic layer | Cube Core | Define metrics, joins, dimensions, and API exposure |
| Agent orchestration | LangGraph | Manage catalog lookup, query, and visualization flow |
| Model layer | OpenAI API | Interpret business intent and synthesize chart specs; requires network access and an approved API key |
| Frontend canvas | Next.js + react-vega | Render Vega-Lite chart widgets dynamically |
| Traditional BI validation | Metabase Community | Confirm metric parity through SQL-based dashboards |

## 6. Functional Requirements

### FR-1: Lakehouse Storage and Querying

1. The system shall read analytical Gold-layer Parquet or Delta files directly from local storage using DuckDB.
2. The platform shall not require a cloud data warehouse for the core PoC execution.
3. The underlying storage engine shall support fast metric aggregation for interactive conversational analytics.
4. Query execution for common aggregate calculations shall be performant enough to support near-real-time prompt response.

### FR-1A: Business Intelligence Functional Scope

The system shall support a business intelligence workflow covering the following three operational domains:

1. Sales Monitoring and Forecasting
   - The system shall provide executive dashboards and conversational analytics for sales trends, performance by region, category, and channel.
   - The system shall support KPI monitoring for gross revenue, net revenue, discount impact, units sold, and order volume.
   - The system shall support forecast-style trend analysis for future revenue and sales momentum based on historical patterns.
   - The system shall allow users to query questions like: "What is monthly revenue by region?", "What is the forecast for Q4 sales?", or "Which category is driving the strongest growth?"

2. Customer Profile Review
   - The system shall provide customer-level segmentation analytics including customer segment, region, order behavior, and value contribution.
   - The system shall support analysis of repeat purchase behavior, customer concentration, and segment-based revenue patterns.
   - The system shall allow users to review customer profiles using dimension attributes such as segment, region, order history, and purchasing behavior.
   - The system shall allow questions like: "Who are our top customers by net revenue?" or "What is the revenue mix by customer segment?"

3. Product Inventory Management
   - The system shall support product and inventory analytics such as stock coverage, product category mix, low-stock signal identification, and product contribution to revenue.
   - The system shall allow analysis of product performance by category, subcategory, sales velocity, and inventory health.
   - The system shall support monitoring of high-selling vs low-selling items and identify product demand trends.
   - The system shall allow questions like: "Which products have low inventory but high sales velocity?" or "What is product revenue by category?"

### FR-2: Metric Governance and Semantic Layer

1. Metrics, dimensions, joins, and filters shall be defined in version-controlled configuration files.
2. Cube Core shall act as the canonical semantic layer for metric definitions.
3. The semantic layer shall expose a REST API for AI-driven metric retrieval.
4. The semantic layer shall expose a Postgres SQL API for BI validation and dashboard connectivity.
5. The semantic layer shall expose MCP endpoints for agentic integration.
6. The same metric definition shall yield equivalent output regardless of whether it is retrieved through REST or SQL interfaces.

### FR-3: Natural Language Query Resolution

1. The system shall accept business questions in plain English.
2. The agent shall inspect available metric metadata before executing a query.
3. The agent shall map business terms such as revenue, sales, units, region, and category to governed semantic definitions.
4. The system shall reject prompts unrelated to the available analytics domain in a polite and structured manner.
5. Ambiguous prompts shall be resolved through catalog inspection and default mapping rules.

### FR-4: Agent Orchestration and Execution Flow

1. The agent shall use LangGraph to manage a deterministic ReAct execution cycle.
2. The execution flow shall include:
   - catalog discovery
   - query execution
   - visualization specification synthesis
3. The system shall request and inspect catalog metadata before generating a query.
4. If a generated spec fails validation, the agent shall retry up to a defined limit before surfacing an error.
5. The agent shall route requests to the right metric, dimension, and filter set based on the business question.

### FR-5: Visualization Generation

1. The frontend shall render charts from declarative Vega-Lite JSON rather than hardcoded chart components.
2. Supported chart styles shall include:
   - vertical bar charts
   - horizontal bar charts
   - line and time-series charts
   - stacked area charts
   - KPI cards
3. Users shall be able to modify the visualization through a conversational instruction without re-querying the semantic layer when the change is only visual.
4. The dashboard shall support a dynamic layout grid for resizing, reordering, and closing charts.

### FR-6: Traditional BI Validation

1. Metabase shall connect to the same semantic layer and validate the same metrics via SQL.
2. Users shall be able to compare AI-generated metric outputs against conventional BI outputs.
3. Metric parity shall be validated for equivalent filters and dimensions.
4. The stack shall prove that the AI canvas and traditional BI are reading from the same source-of-truth metrics.

### FR-7: Local Runtime and LLM Provider

1. The PoC shall run without Docker, Docker Compose, WSL, or another container runtime as a prerequisite.
2. Cube Core, the LangGraph agent, the Next.js frontend, and Metabase shall be started as native local processes or services using documented setup and startup instructions.
3. DuckDB shall be embedded in the component that queries the Gold-layer files; it shall not require a separately hosted database service for the PoC.
4. The PoC shall use the OpenAI API as its LLM provider. The local application and lakehouse data remain on the developer host, while prompts sent for model inference use the external OpenAI service.
5. The OpenAI API key shall be supplied through local environment configuration, excluded from version control, and never embedded in source code or committed configuration.
6. The PoC shall not send sensitive, confidential, or identifying source data to the external LLM service; prompts and context shall be limited to the minimum needed for inference.

## 7. Domain Model

The current PoC domain is e-commerce analytics, with a star schema built around sales transactions and operational monitoring across commerce functions.

### Core Entities

- Customers
- Products
- Orders
- Sales fact table
- Inventory and demand tracking

### Key Fact and Measures

- gross_revenue
- total_discount
- net_revenue
- total_units_sold
- order_line_count
- average_order_value
- inventory_on_hand
- stock_coverage_days
- product_sales_velocity
- forecasted_sales_amount

### Dimensional Attributes

- customer_segment
- region
- category
- subcategory
- order_status
- payment_method
- order_date
- product_status
- inventory_status
- customer_profile_tier

### BI Use Case Mapping

- Sales monitoring: revenue, units sold, demand trend, order count, regional performance
- Forecasting: predicted sales trajectory and trend comparison against baseline
- Customer profile review: customer segmentation, contribution by segment, repeat orders, region mix
- Product inventory management: inventory availability, product demand, item turnover, stock health

## 8. Example Business Metric Rules

- Revenue queries default to net revenue unless gross revenue is explicitly requested.
- Unit-based questions map to total quantity sold.
- Region-based questions resolve through customer-region dimension joins.
- Category questions resolve to product category dimensions.
- Revenue validation should normally exclude non-completed orders unless the user specifically asks otherwise.
- Sales monitoring and forecast questions should resolve to trend, period, and KPI measures rather than raw transaction details.
- Customer profile reviews should prioritize segment, region, and customer contribution analysis as the primary dimensions.
- Inventory questions should resolve to stock coverage, product demand, and category/subcategory performance rather than generic order summaries.

## 9. Quality Gates / Acceptance Criteria

### Gate 1: End-to-End Functional Flow

A user prompt shall successfully pass through the pipeline:

DuckDB -> Cube -> LangGraph -> Vega-Lite -> Next.js

The end-to-end path must execute within the PoC target time window.

### Gate 2: Zero Hardcoded Charts

The dashboard must render nontrivial charts by interpreting incoming declarative Vega-Lite payloads. No custom chart logic should be required for standard chart types.

### Gate 3: Metric Consistency

The metric values displayed in the AI dashboard must match those displayed in Metabase for the same dimension filters and metric definitions.

### Gate 4: Semantic Resolution Quality

A high percentage of benchmark prompts must resolve to the correct semantic measure and dimension combination.

### Gate 5: BI Capability Coverage

The demonstrator must successfully support business questions in all of the following categories:

- sales monitoring and trend analysis
- sales forecasting and forward-looking momentum assessment
- customer profile review and segment analysis
- product inventory review and stock-health analysis

## 10. Non-Functional Requirements

### Performance

- the local stack must support near-real-time analytical interaction
- query execution should remain responsive for common prompt-driven analysis

### Maintainability

- metric definitions must be code-first and version-controlled
- the system must separate semantic modeling, agent reasoning, and visual rendering responsibilities

### Observability

- errors must be visible in logs and surfaced clearly in the UI or orchestration layer
- validation failures must support quick diagnosis of query or spec issues

### Portability

- application services must run locally as native processes without requiring a container runtime
- setup, configuration, and startup instructions must be documented for the supported local development environment
- lakehouse data and query execution remain local; the OpenAI API is the explicitly approved external runtime dependency for LLM inference

### Two-Developer Delivery and Coordination

- **NFR-TEAM-1 — Bounded ownership:** Each delivery unit shall have one accountable developer (Developer A or Developer B), a defined outcome, and explicit acceptance checks. The ownership map in Section 10.1 is the baseline for the two-developer PoC.
- **NFR-TEAM-2 — Parallel slices:** Work shall be divided into independently testable slices wherever dependencies allow. Each phase shall identify its user stories, units, accountable owner, dependencies, and integration handoff.
- **NFR-TEAM-3 — Shared contracts first:** Before parallel implementation, both developers shall agree on relevant data schemas, metric/API contracts, request/response payloads, and file or service boundaries. Contract changes shall be communicated to the other owner before implementation proceeds.
- **NFR-TEAM-4 — Integration gates:** A dependent slice shall not be considered complete until its documented handoff is consumed and integration checks pass. Phase exits shall include evidence for the phase acceptance criteria and cross-slice integration.
- **NFR-TEAM-5 — Avoid conflicting ownership:** A shared file or component shall have one designated owner at a time. The other developer may review or contribute through an agreed handoff; parallel edits to the same artifact are avoided.
- **NFR-TEAM-6 — Review and traceability:** Each unit shall link to one or more requirements/stories and have a test or other verifiable acceptance check. The non-owning developer shall review the integrated outcome where feasible.
- **NFR-TEAM-7 — Roles are placeholders:** Developer A and Developer B denote delivery ownership, not named individuals or fixed job titles. The team may swap owners before a phase starts, provided every unit retains a single accountable owner and dependencies remain explicit.

### 10.1 Two-Developer User Story and Unit Ownership Baseline

The following story/unit allocation is the planning baseline for a team of two. Owners may sequence work within their slice, but must observe the handoff gates in the phased requirements. Stories are delivery slices aligned to the functional requirements; units are the independently buildable/testable work items.

| Phase | Story | User story outcome | Unit(s) | Owner | Dependency / handoff |
|---|---|---|---|---|---|
| 1 | P1-US-1 | As a developer, I can reproducibly generate and ingest synthetic source data so downstream models have stable inputs. | P1-U1: synthetic data generator and source contract; P1-U2: Bronze ingestion and lineage | Developer A | Publish schemas, keys, seed/configuration, and Bronze locations for Developer B. |
| 1 | P1-US-2 | As an analytics consumer, I can use clean, documented Gold models for sales, customer, and inventory analysis. | P1-U3: Silver transformations and data-quality rules; P1-U4: Gold facts/dimensions and sample queries | Developer B | Starts from the agreed source/Bronze contract; return Gold schema, measures, grain, and sample outputs for Phase 2. |
| 2 | P2-US-1 | As an analytics consumer, I can discover governed metrics and dimensions over the Gold model. | P2-U1: Cube model and metric catalog | Developer A | Agree Gold-to-semantic mapping; hand off stable metric/dimension names and definitions. |
| 2 | P2-US-2 | As an agent or BI consumer, I can access the same governed metrics through supported interfaces. | P2-U2: REST/MCP/SQL interfaces; P2-U3: cross-interface parity checks | Developer B | Integrate against P2-U1 contract; hand off endpoint/query examples and parity evidence. |
| 3 | P3-US-1 | As a business user, I can ask an analytics question and receive a governed, interpretable result. | P3-U1: catalog resolution, query orchestration, and agent flow | Developer A | Depends on Phase 2 interfaces; agree request/result/error contract with Developer B. |
| 3 | P3-US-2 | As a business user, I can see and arrange dynamically generated visualizations with concise insights. | P3-U2: Next.js chat/canvas and Vega-Lite rendering; P3-U3: visualization and UI integration tests | Developer B | Consumes the agreed agent result/spec contract; integrate end-to-end with P3-U1. |
| 4 | P4-US-1 | As a business user, I can review sales and customer performance in a traditional dashboard. | P4-U1: sales/customer dashboard views | Developer A | Uses approved semantic/SQL metrics; provide query and metric mapping for parity review. |
| 4 | P4-US-2 | As a business user, I can monitor product and inventory health and compare dashboard values to governed metrics. | P4-U2: inventory dashboard views; P4-U3: Metabase setup and cross-view parity evidence | Developer B | Depends on Phase 2 SQL interface and shared metric definitions; hand off final parity evidence. |

At each phase kickoff, confirm the owner, unit boundaries, shared contract, and integration gate before implementation. The phase-specific files define the concrete acceptance checks and handoffs.

## 11. Technical Constraints

- use open-source software for the application and analytics components; the OpenAI API is a hosted, non-open-source dependency
- the OpenAI API is the selected LLM provider for this PoC; local Ollama is not required
- Docker, Docker Compose, WSL, and containerization are not prerequisites for local development or PoC execution
- the PoC should prioritize a minimal, documented, reproducible native local setup
- the semantic layer should remain the single source of truth for metrics

These deployment and LLM decisions supersede conflicting containerization or local-Ollama options in the source documents listed in Section 13 for this PoC.

## 12. Success Criteria

The PoC is successful if it demonstrates all of the following:

1. a business user can ask a natural-language analytics question
2. the AI agent resolves the request to the correct metric and dimension set
3. the query executes through a governed semantic layer
4. the result is rendered as a valid visualization without custom chart code
5. the result is validated against a traditional BI dashboard with matching numbers

## 13. Source Inputs Used

This refined requirement consolidates the following source artifacts:

- Agentic-BI-Functional-Requirement
- Agentic-BI-gates-spec
- Agentic-BI-poc-domain-specific-guide
- Agentic-BI-Technical-Spec-Guide

## 14. Summary

The refined requirement for the Agentic BI PoC is a local-first, open-source analytics system that enables conversational business intelligence through an AI agent, a governed semantic layer, and a dynamic visualization canvas. The project focuses on proving that natural-language analytics can be both highly usable and trustworthy when metric definitions are controlled centrally and validated through traditional BI workflows.
