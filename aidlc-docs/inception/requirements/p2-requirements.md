# Phase 2 Requirements — Semantic Layer Implementation

> **Scope amendment (2026-09-30):** The Cube semantic-layer, MCP, SQL, and cross-interface requirements below are superseded for the current Phase 2 delivery. The approved scope is the local Gold REST API in [phase-2 requirements](../../../requirements/phased/phase-2-semantic-layer-mcp-rest.md), with implementation details in [P2-U2 code plan](../../construction/plans/p2-u2-code-generation-plan.md). Cube remains an optional existing prototype only.

## Intent Analysis
- **User request**: Start AIDLC for Phase 2 and keep design and units simple for one data engineer, with a rapid implementation focus.
- **Request type**: Brownfield feature implementation extending the completed Phase 1 lakehouse.
- **Scope**: An open-source, local-first semantic layer over Gold data; Cube Core service; REST, MCP, and SQL-compatible access; and cross-interface validation.
- **Complexity**: Moderate because several interfaces must share metric semantics, but implementation and delivery are limited to a single local PoC.
- **Delivery ownership**: One data engineer owns all work sequentially. Keep design artifacts concise and minimize the number of units without removing essential contract and parity checks.

## Decisions and Constraints
- **Source of truth**: Phase 1 Gold Parquet data, after correcting the inventory calculations selected in Question 2.
- **Sales eligibility**: Use completed orders only, consistent with the Phase 1 business rule. Verify and correct the Gold sales output if necessary before exposing semantic measures.
- **Inventory semantics**: Correct or extend Gold so inventory velocity reflects sales demand and coverage days reflects on-hand inventory divided by a documented daily demand rate. Define the demand lookback, snapshot alignment, and zero/no-history behavior during Functional Design; do not present the current stock-to-reorder ratio as coverage days.
- **Forecasts**: Defer forecast measures in Phase 2 until a forecast Gold dataset is available.
- **Runtime**: Cube Core runs as a native local service and reads local Gold Parquet through DuckDB. Docker, Docker Compose, WSL, or another container runtime must not be prerequisites.
- **Open semantic approach**: Use the open-source Cube Core semantic layer with version-controlled model definitions and open data/protocol formats where practical. Do not require Cube Cloud, a hosted semantic service, or a proprietary runtime. Verify the chosen Cube Core version's license and that required interfaces can run locally before implementation; favor a small adapter over adding another semantic platform.
- **Governance**: Cube is the canonical definition of metrics, dimensions, joins, and filters. Do not maintain competing metric formulas in REST, MCP, or SQL adapters.
- **Extensions**: Property-Based Testing, Security Baseline, and Resiliency Baseline remain disabled for this PoC. Focused conventional tests and applicable baseline-safe practices still apply.

## Functional Requirements

### P2-FR-1: Governed Semantic Catalog
1. Define the semantic model and business metrics in version-controlled Cube model files over the corrected Gold contract.
2. Expose discoverable metadata for measures, dimensions, filters, and joins.
3. Keep fact measures distinct from descriptive attributes and document table grain, keys, and relationships.

### P2-FR-2: Metrics and Dimensions
1. Support sales measures for gross sales, discounts, net sales, units sold, order volume, and customer contribution using completed orders only.
2. Define order volume as distinct orders, not order lines. Define customer contribution from net sales by customer and expose its share of total net sales where supported by Cube's governed query semantics.
3. Support customer repeat-purchase analysis using distinct completed orders by customer.
4. Support inventory on-hand and low-stock analysis at product-day snapshot grain. Add corrected sales-velocity and stock-coverage measures using documented Gold calculations.
5. Expose time, customer, product, category/subcategory, region, channel, and stock-state dimensions where present in Gold. Support daily/monthly/quarterly/yearly time roll-up from the Gold date fields; a persisted date dimension is not required unless design finds it necessary.
6. Do not publish forecast measures until forecast Gold data is available.

### P2-FR-3: REST Access
1. Provide a local REST interface for semantic catalog discovery and governed metric queries.
2. Return structured metadata and result payloads suitable for BI applications and downstream agents.
3. Restrict queries to validated semantic definitions and approved dimensions and filters.

### P2-FR-4: MCP Access
1. Provide MCP discovery and governed metric-query operations for agent consumers.
2. Route MCP execution through the canonical semantic model; do not accept arbitrary SQL or bypass semantic validation.
3. Demonstrate that representative MCP queries return the same governed results as equivalent REST queries.

### P2-FR-5: SQL-Compatible BI Access
1. Provide a documented SQL-compatible path for Metabase or equivalent local BI validation.
2. Ensure SQL BI queries use the same governed metric definitions as REST and MCP; do not introduce separate business formulas.
3. Document the local connection method and a representative query.

### P2-FR-6: Cross-Interface Parity
1. Verify equivalent measures and filters produce equivalent results through REST, MCP, and the SQL-compatible path.
2. Include representative sales, customer, and inventory queries with expected results and concise setup examples.
3. Keep parity checks and examples within the interface-integration deliverable rather than creating a separate implementation unit.

## Non-Functional Requirements and Constraints
- **Local-first**: Native host processes and local files; no container runtime prerequisite.
- **Data access**: Read only the required local Gold data through DuckDB; make the data path configurable and document it.
- **Metric integrity**: Validate model/query inputs and avoid arbitrary SQL execution through MCP or REST.
- **Privacy and credentials**: Use synthetic project data; keep credentials in local environment configuration and out of source control; do not send source records to an external LLM.
- **Maintainability**: Keep the Cube model and integration configuration inspectable and version controlled. Prefer the minimum components needed for the required interfaces; avoid additional semantic frameworks and proprietary dependencies.
- **Testability**: Add focused model, endpoint, and parity tests for changed behavior. Verify native startup and shutdown locally.
- **Extensions**: Property-based, security-baseline, and resiliency-baseline extensions are disabled. Their extension-specific rules are not applicable; ordinary input validation, safe configuration, and focused testing remain expected.

## Acceptance Criteria
1. Cube Core starts natively using documented local setup and reads the configured Gold data through DuckDB without Docker, WSL, or a container runtime.
2. Version-controlled semantic models expose the agreed metrics, dimensions, grains, and relationships over corrected Gold outputs.
3. Sales metrics include completed orders only; inventory velocity and coverage have documented, corrected business meanings and edge-case behavior.
4. Forecast measures are excluded until a forecast Gold dataset is available.
5. Consumers can discover catalog metadata and query governed metrics through REST and MCP.
6. A SQL-compatible local BI validation path uses the same governed metric definitions.
7. Focused parity checks demonstrate matching results for equivalent measures and filters across available interfaces.
8. Local setup, data path, endpoints, and representative query examples are documented for Phase 3 and Phase 4 consumers.
9. The selected semantic service and required interfaces run locally using an open-source implementation without requiring a hosted or proprietary semantic platform.

## Delivery Boundaries
- Preserve the outcomes of P2-US-1 (discover governed metrics) and P2-US-2 (consume the same metrics through interfaces).
- Use one data engineer and sequential handoffs. The preliminary lean shape is a semantic model/catalog slice followed by a combined service-interface/parity slice; final stage and unit recommendations belong in Workflow Planning.
- Do not include a Phase 3 conversational agent, Phase 4 dashboard, production deployment, or production forecasting in this scope.

## Design Items to Resolve Before Implementation
- Select and validate the native Cube Core DuckDB configuration and local Gold path.
- Verify the selected Cube Core version's license and local availability of the required REST, MCP, and SQL-compatible access paths.
- Select a compatible local SQL/BI connection path that preserves Cube metric definitions.
- Determine the smallest MCP integration that supports governed discovery and query execution.
- Specify the inventory demand lookback, snapshot alignment, and behavior for zero or insufficient sales history.
- Confirm Cube model/query validation and parity test commands for the chosen local setup.
