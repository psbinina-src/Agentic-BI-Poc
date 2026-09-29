# Phase 4: Static Business Intelligence Dashboard Implementation

## 1. Objective

Deliver a conventional static BI dashboard experience built on top of the same governed data and semantic definitions used by the Agentic BI workflow. This phase validates the business value of the model through a traditional dashboard-first view.

## 2. Scope

This phase covers the creation of a standard dashboard that presents business results in a familiar analytical layout, including:

- sales monitoring panels
- customer profile views
- product and inventory dashboards
- trend and performance summaries

### Local Runtime

1. Run Metabase Community using an approved native local installation or launcher; Docker, Docker Compose, WSL, and a container runtime are not prerequisites.
2. Document the local Metabase startup method and its connection to the semantic layer's SQL-compatible endpoint.

## 2.1 Two-Developer Stories, Units, and Handoffs

| Story | User story outcome | Unit(s) | Owner | Dependency / acceptance handoff |
|---|---|---|---|---|
| P4-US-1 | As a business user, I can review sales and customer performance in a traditional dashboard. | P4-U1: sales and customer dashboard views, queries, and metric mapping | Developer A | Depends on approved Phase 2 semantic/SQL definitions; verify key dashboard values and filters against the governed metrics and provide expected results for parity review. |
| P4-US-2 | As a business user, I can monitor product and inventory health and compare dashboard values to governed metrics. | P4-U2: inventory dashboard views; P4-U3: Metabase setup, shared metric parity checks, and validation report | Developer B | Depends on the Phase 2 SQL interface and inventory measures; verify low-stock/high-velocity views, local setup, and parity against the same metric definitions. |

**Integration gate:** Agree dashboard metric names, filters, and expected results before building views. Integrate the sales/customer and inventory slices in Metabase, then jointly verify representative results against the semantic layer and, when available, the Agentic BI flow before Phase 4 acceptance.

## 3. Functional Requirements

### P4-FR-1: Dashboard Layout

1. The system shall provide a static or semi-static dashboard layout for business users.
2. The dashboard shall include clear summary tiles, charts, and table views for key metrics.
3. Layout shall be structured around the primary BI use cases:
   - sales
   - customer profile
   - inventory management

### P4-FR-2: Sales Dashboard

1. The sales dashboard shall show revenue growth, trend curves, and regional/category performance.
2. Users shall be able to review KPIs for net revenue, gross revenue, units sold, and order volume.
3. Forecast comparison views shall be available where applicable.

### P4-FR-3: Customer Dashboard

1. The customer dashboard shall show customer segmentation summaries.
2. The dashboard shall highlight revenue contribution by segment and region.
3. Repeat purchase and profile-based analysis shall be included where feasible.

### P4-FR-4: Inventory Dashboard

1. The inventory dashboard shall display stock health and product demand insights.
2. The dashboard shall identify products at risk of low stock or high sales velocity.
3. Category and subcategory performance shall be visible in summarized views.

### P4-FR-5: Consistency With Semantic Layer

1. The static dashboard shall use the same semantic definitions and approved metrics as the Agentic BI workflow.
2. Shared KPIs must align with the same source-of-truth logic.
3. The dashboard shall serve as a validation layer for metric parity across interfaces.

## 4. Dashboard Output Expectations

The dashboard shall support business users with:

- KPI scorecards
- trend visualizations
- segmentation views
- product performance tables
- inventory health monitoring

## 5. Acceptance Criteria

The phase is complete when:

1. a static BI dashboard exists for the core business use cases
2. sales, customer, and inventory views are all represented
3. the dashboard uses the same metric definitions as the semantic layer
4. the dashboard can be used as a validation comparison point against the Agentic BI view
5. Metabase connects to the locally running semantic layer using the documented non-containerized setup

## 6. Deliverables

- static dashboard design and layout
- sales dashboard views
- customer review dashboard views
- product inventory dashboard views
- dashboard validation report against semantic metrics
