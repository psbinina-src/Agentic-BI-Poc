# Phase 3: Agentic BI Implementation

## 1. Objective

Build the conversational analytics experience that can interpret business questions, resolve them to semantic metrics, execute the correct query, and render analytical visuals. This phase brings together the lakehouse, semantic layer, and AI reasoning stack into an Agentic BI workflow.

## 2. Scope

This phase includes:

- natural-language business question handling
- semantic catalog discovery
- query orchestration and metric resolution
- chart spec generation
- dynamic dashboard widget rendering
- AI-driven insights and summaries

### Local Runtime and LLM Provider

1. Run the LangGraph agent and Next.js frontend as native local processes; Docker, Docker Compose, WSL, and a container runtime are not prerequisites.
2. Use the OpenAI API as the PoC LLM provider. Model inference requires network access and an approved API key supplied through local environment configuration.
3. Do not commit API keys or send sensitive, confidential, or identifying source data to the LLM provider. Keep lakehouse storage and DuckDB query execution local.
4. Document the local service endpoints and startup order for the frontend, agent, and semantic layer.

## 2.1 Two-Developer Stories, Units, and Handoffs

| Story | User story outcome | Unit(s) | Owner | Dependency / acceptance handoff |
|---|---|---|---|---|
| P3-US-1 | As a business user, I can ask an analytics question and receive a governed, interpretable result. | P3-U1: catalog discovery, intent/metric resolution, query orchestration, and agent flow | Developer A | Depends on Phase 2 interfaces. Agree the agent request/result/error contract with Developer B; verify representative sales, customer, and inventory questions use governed metrics and handle invalid/ambiguous requests. |
| P3-US-2 | As a business user, I can see and arrange dynamically generated visualizations with concise insights. | P3-U2: chat/canvas, Vega-Lite rendering, and widget interactions; P3-U3: UI and end-to-end integration checks | Developer B | Consume the agreed agent result/spec contract; verify valid declarative specs render, supported interactions work, and errors are presented clearly. |

**Integration gate:** Agree the agent-to-UI payload, chart-spec constraints, and error states before parallel implementation. Integrate against the live semantic interface and validate the complete question-to-visualization path for all three business domains before Phase 3 acceptance.

## 3. Functional Requirements

### P3-FR-1: Conversation Interface

1. The system shall accept plain-English business questions from end users.
2. The user experience shall include a chat-style interface for business analytics inquiry.
3. The agent shall interpret user intent and identify the relevant measure, dimensions, and filters.

### P3-FR-2: Catalog Resolution

1. The agent shall inspect semantic metadata before generating or executing a query.
2. The system shall map business terms such as revenue, forecast, inventory, customer segment, and product category to the correct semantic objects.
3. Ambiguous requests shall be resolved using available metadata and default business logic.

### P3-FR-3: Query Execution

1. The agent shall use the semantic layer to retrieve the correct metric data.
2. The system shall execute approved metric queries without bypassing semantic governance.
3. Query execution shall support sales, customer, and inventory-driven questions.

### P3-FR-4: Visualization Generation

1. The system shall convert query results into a valid Vega-Lite or equivalent declarative visualization specification.
2. Generated visualizations shall support:
   - trend charts
   - bar charts
   - KPI cards
   - comparison charts
   - segmentation views
3. Visualization generation shall not require hardcoded chart implementations for standard business visuals.

### P3-FR-5: Dynamic Dashboard Experience

1. The frontend shall render chart widgets dynamically within a user interface canvas.
2. Users shall be able to resize, move, and close chart widgets.
3. Generated outputs shall be compatible with the conversational BI view and the static dashboard view.

### P3-FR-6: Insight Summary

1. The system shall provide concise insight summaries after chart generation.
2. The insights shall explain the key business signal behind the result.
3. Summaries shall support business interpretation such as sales acceleration, segment concentration, or inventory risk.

## 4. Agentic BI Use Cases

The Agentic BI workflow shall support:

- "Show monthly sales by region."
- "Forecast revenue for the next quarter."
- "Which customer segment contributed the most net revenue?"
- "Which products are running low on inventory and high in demand?"
- "Compare sales trend by category across the last six months."

## 5. Acceptance Criteria

The phase is complete when:

1. the user can ask natural-language BI questions
2. the system resolves questions to valid semantic metrics and dimensions
3. the result is generated via the semantic layer and rendered as a visualization
4. insight summaries are presented to the user
5. sales, customer, and inventory use cases are all supported in the conversational UI
6. the agent can call the OpenAI API using locally configured credentials without exposing the key in source control

## 6. Deliverables

- conversational BI interface
- semantic-to-visual query orchestration flow
- generated chart widgets
- insight summary layer
- validation samples across the business domains
