# Phase 3: Prompt-Driven Agentic BI Dashboard

## 1. Objective

Build a small local prompt-driven analytics dashboard. A lightweight Python agent uses OpenAI tool calls to discover Gold metadata and request bounded aggregate data from the completed Phase 2 REST API, then returns an insight and a validated Vega-Lite chart.

## 2. Scope

This phase includes:

- natural-language business question handling
- Phase 2 Gold catalogue/field discovery
- query orchestration through the Phase 2 REST API only
- chart spec generation
- one prompt-generated chart at a time in a simple dashboard
- AI-driven insights and summaries

Keep this increment deliberately small: one local Python service and a static HTML/CSS/JavaScript dashboard. LangGraph, Next.js, Cube, MCP, user-managed chart canvases, and multiple movable/resizable widgets are deferred. The agent uses Gold fields and generic aggregates; it does not add a separate semantic metric layer.

### Local Runtime and LLM Provider

1. Run the Python agent/API and static dashboard as a native local process; Docker, Docker Compose, WSL, and a container runtime are not prerequisites.
2. Use the OpenAI API as the PoC LLM provider. Model inference requires network access and an approved API key supplied through local environment configuration.
3. Do not commit API keys or send sensitive, confidential, or identifying source data to the LLM provider. Keep lakehouse storage and DuckDB query execution local.
4. The agent shall call only the Phase 2 local Gold REST API for dataset discovery and data access. Bind the Phase 3 service to `127.0.0.1`; document startup order and local endpoints.

## 2.1 Single-Engineer Stories, Units, and Handoffs

| Story | User story outcome | Unit(s) | Owner | Dependency / acceptance handoff |
|---|---|---|---|---|
| P3-US-1 | As a business user, I can ask an analytics question and receive an interpretable result from Gold data. | P3-U1: OpenAI tool-calling flow over the Phase 2 API | One data engineer | Verify metadata discovery, bounded aggregate queries, and clear handling of unsupported questions. |
| P3-US-2 | As a business user, I can view a generated chart and concise insight for my question. | P3-U1: prompt dashboard and Vega-Lite rendering | One data engineer | Verify generated specs use returned fields only and errors are visible. |

**Integration gate:** Use the stable Phase 2 REST contract. Validate the question-to-visualization path for sales, customer segments/regions, and inventory; unsupported forecasts must be identified as unavailable rather than invented.

## 3. Functional Requirements

### P3-FR-1: Conversation Interface

1. The system shall accept plain-English business questions from end users.
2. The user experience shall include a chat-style interface for business analytics inquiry.
3. The agent shall interpret user intent and identify the relevant measure, dimensions, and filters.

### P3-FR-2: Catalog Resolution

1. The agent shall inspect the Phase 2 dataset catalogue and field metadata before querying.
2. The agent shall map business terms to available Gold fields and documented relationships; it shall not invent absent measures or datasets.
3. Ambiguous requests shall be clarified briefly or answered with the available metadata; unsupported requests, including forecasts without Gold forecast data, shall be declined clearly.

### P3-FR-3: Query Execution

1. The agent shall use only the Phase 2 REST API for Gold catalogue and data access.
2. The API shall receive bounded aggregate queries; Phase 3 shall not execute SQL or read Parquet directly.
3. Query execution shall support sales, customer-segment/region, and inventory questions using available Gold fields and approved joins.

### P3-FR-4: Visualization Generation

1. The system shall convert query results into a valid Vega-Lite or equivalent declarative visualization specification.
2. Generated visualizations shall support:
   - trend charts
   - bar charts
   - comparison charts
   - segmentation views
3. Visualization generation shall not require hardcoded chart implementations for standard business visuals. KPI cards and multi-chart output are deferred.

### P3-FR-5: Dynamic Dashboard Experience

1. The frontend shall render one validated Vega-Lite chart for the latest prompt response.
2. This increment does not require move/resize/close widget interactions or a multi-chart canvas.
3. Chart encodings shall reference only fields returned by the Phase 2 API; reject arbitrary URLs, expressions, and unsupported marks.

### P3-FR-6: Insight Summary

1. The system shall provide concise insight summaries after chart generation.
2. The insights shall explain the key business signal behind the result.
3. Summaries shall support business interpretation such as sales acceleration, segment concentration, or inventory risk.

## 4. Agentic BI Use Cases

The Agentic BI workflow shall support:

- "Show daily net sales by region for the last month."
- "Which customer segment contributed the most net revenue?"
- "Which products are running low on inventory and high in demand?"
- "Compare net sales by product category."

## 5. Acceptance Criteria

The phase is complete when:

1. the user can ask natural-language BI questions
2. the agent discovers Gold metadata and queries only through the Phase 2 API
3. a valid result is rendered as a visualization and unsupported/ambiguous requests are handled clearly
4. insight summaries are presented to the user
5. sales, customer-segment/region, and inventory use cases are supported in the prompt dashboard; forecast requests are not fabricated
6. the agent can call the OpenAI API using locally configured credentials without exposing the key in source control

## 6. Deliverables

- conversational BI interface
- semantic-to-visual query orchestration flow
- generated chart widgets
- insight summary layer
- validation samples across the business domains
