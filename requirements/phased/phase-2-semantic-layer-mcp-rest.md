# Phase 2: Semantic Layer Implementation

## 1. Objective

Implement the business semantic layer on top of the lakehouse Gold model so that analytics consumers can access governed metrics through standard interfaces. This phase creates the metric layer that provides a single source of truth for BI, dashboards, and AI query interpretation.

## 2. Scope

This phase covers:

- metric definitions for sales, customer, and inventory analytics
- semantic modeling over the Gold layer
- REST API exposure for programmatic integration
- MCP support for agentic consumption
- SQL-compatible access for traditional BI validation

### Local Runtime

1. Run Cube Core as a native local service; Docker, Docker Compose, WSL, and a container runtime are not prerequisites.
2. Configure the semantic service to read the locally stored Gold-layer data through DuckDB, and document the local data path and service endpoints.

## 2.1 Two-Developer Stories, Units, and Handoffs

| Story | User story outcome | Unit(s) | Owner | Dependency / acceptance handoff |
|---|---|---|---|---|
| P2-US-1 | As an analytics consumer, I can discover governed metrics and dimensions over the Gold model. | P2-U1: Cube model, Gold-to-semantic mapping, and metric catalog | Developer A | Agree the Gold schema, grain, and metric definitions; verify catalog metadata and representative metric queries, then publish stable semantic names and definitions. |
| P2-US-2 | As an agent or BI consumer, I can access the same governed metrics through supported interfaces. | P2-U2: REST, MCP, and SQL interfaces; P2-U3: cross-interface parity checks and setup examples | Developer B | Build against the agreed semantic contract; verify supported endpoint/query examples and equivalent results across available interfaces; publish endpoint and parity evidence for Phases 3 and 4. |

**Integration gate:** Finalize the Gold mapping and semantic naming contract before interface integration. Developer A provides representative expected results; Developer B exercises the interfaces against those results. Phase 2 is accepted only after the interfaces start using the documented native setup and parity checks pass.

## 3. Functional Requirements

### P2-FR-1: Semantic Metric Definitions

1. The system shall define metrics in a version-controlled semantic layer.
2. The semantic layer shall include standardized definitions for:
   - sales revenue
   - units sold
   - order volume
   - customer contribution
   - forecast measures
   - inventory health measures
3. Measures shall be built using the Gold layer as the source of truth.
4. The semantic model shall distinguish between fact measures and descriptive attributes.

### P2-FR-2: Data Modeling for Semantic Queries

1. The semantic layer shall expose dimensions and facts for:
   - time
   - customer
   - product
   - category/subcategory
   - region
   - inventory and stock state
2. The semantic layer shall support drill-down and roll-up queries across business dimensions.
3. The model shall support all BI questions required by the PoC use cases.

### P2-FR-3: API Integration

1. The semantic layer shall expose a REST API for querying catalog metadata and metric results.
2. The REST interface shall provide structured responses suitable for downstream AI agents and applications.
3. The semantic layer shall expose metadata describing measures, dimensions, filters, and joins.
4. All API responses shall be consistent with the underlying Gold-layer definitions.

### P2-FR-4: MCP Integration

1. The system shall support MCP-based integration for AI agents to discover and query metrics.
2. The MCP interface shall allow a conversational agent to access semantic metadata and execute governed analytical queries.
3. The MCP layer shall be restricted to validated semantic definitions and approved data access patterns.

### P2-FR-5: Traditional BI Connectivity

1. The semantic layer shall expose a SQL-compatible interface for tools such as Metabase.
2. The SQL layer shall serve the same metric logic used by AI-driven queries.
3. Traditional BI consumers shall be able to validate the same results as the Agentic BI front end.

### P2-FR-6: Metric Consistency

1. The system shall ensure that identical filters and measures return consistent results across API, MCP, and SQL interfaces.
2. Metric definitions shall be centrally controlled to avoid divergence between business intelligence tools.

## 4. Semantic Use Cases

### Sales Analytics

- total sales by region
- trend by month and quarter
- product category contribution
- forecast vs actual comparison

### Customer Analytics

- customer segment performance
- customer contribution ranking
- region-based customer profile analysis
- repeat customer behavior

### Inventory Analytics

- stock coverage by product and category
- inventory health summary
- product demand vs available stock
- low-stock and high-velocity product analysis

## 5. Acceptance Criteria

The phase is complete when:

1. semantic definitions exist for the required BI use cases
2. the semantic layer exposes REST and/or MCP endpoints
3. SQL-driven BI validation is possible against the same semantic layer
4. metric outputs match across consumers for equivalent requests
5. the layer is ready for Agentic BI integration
6. Cube Core starts and serves its required interfaces using the documented native local setup

## 6. Deliverables

- semantic metric catalog
- model definitions for measures/dimensions
- REST integration layer
- MCP integration layer
- SQL endpoint configuration for BI validation
- validation report proving metric parity
