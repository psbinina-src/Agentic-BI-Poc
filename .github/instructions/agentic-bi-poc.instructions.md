---
applyTo: "**"
---

# Agentic BI Test PoC — Project Steering

## Purpose and Domain

This repository is a local-first proof of concept for governed, natural-language business intelligence. The current example domain is e-commerce: sales monitoring and forecasting, customer profile review, and product inventory management. Treat this as project context, not as proof that every feature is already implemented.

## Intended Architecture

Use the refined Agentic BI PoC direction as the starting point when relevant:

- **Data/query:** DuckDB over local Gold-layer Parquet or Delta data.
- **Semantic governance:** Cube Core is the canonical home for metric, dimension, join, and filter definitions.
- **Agent orchestration:** LangGraph coordinates catalog discovery, governed query execution, and visualization-spec generation.
- **LLM:** OpenAI API, configured through local environment variables; never hardcode or commit credentials.
- **Visualization:** Next.js with declarative Vega-Lite specifications (including `react-vega` where applicable), rather than chart-type-specific hardcoded components.
- **Traditional BI validation:** Metabase compares results against the same governed metrics.
- **Runtime:** Keep the PoC local-first and runnable as native host processes; Docker or another container runtime must not be a prerequisite.

Do not assume these components, interfaces, or data files exist yet. Inspect the repository before planning implementation, and propose changes incrementally.

## Metric and Data Integrity

- Define metrics and dimensions once in the semantic layer; do not create competing business definitions in the agent or frontend.
- Inspect catalog metadata before selecting metrics or constructing a query.
- Preserve equivalent metric semantics across REST, SQL, MCP, and visualization flows when those interfaces are implemented.
- Use clear, consistent names for business metrics, dimensions, and filters. Ask rather than guess when a metric definition or source mapping is ambiguous.
- Keep prompts and model context to the minimum needed. Do not send sensitive, confidential, or identifying source data to the external LLM.

## Core Business Measures

Potential governed measures include gross revenue, total discount, net revenue, units sold, order-line count, average order value, inventory on hand, stock-coverage days, product sales velocity, and forecasted sales amount. Candidate dimensions include customer segment, region, product/category, channel, and time. Treat these as candidate concepts until the data model confirms their definitions and availability.

## Implementation and Validation

- Favor deterministic, inspectable agent flows and validate generated queries and Vega-Lite specifications before execution/rendering.
- Handle unsupported or out-of-domain questions politely; do not fabricate results.
- Add or update focused tests for changed behavior. Validate metric parity where a change crosses semantic APIs or BI interfaces.
- Document local setup and startup steps when runtime behavior or prerequisites change.
- Avoid adding infrastructure or production-grade complexity beyond the PoC's demonstrated needs.
