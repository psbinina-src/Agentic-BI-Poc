# P3-U1 Code Generation Plan — Prompt Dashboard over Gold REST

## Scope
One sequential unit for one data engineer. The Phase 3 FastAPI service calls only the Phase 2 Gold REST API; the static dashboard sends prompts and displays a concise answer, insight, table, and one Vega-Lite chart. OpenAI credentials are read from local environment configuration and never committed.

## Generation Steps
- [x] Add optional OpenAI/httpx/dotenv dependencies and local-only runtime configuration.
- [x] Implement Gold catalogue/field discovery and bounded aggregate query tools over the Phase 2 API; validate documented joins, fields, key restrictions, ordering, and result limits.
- [x] Implement OpenAI tool-call orchestration and validate model answer and Vega-Lite chart fields/marks before returning a response.
- [x] Build a responsive static prompt dashboard with suggested questions, status/errors, insights, chart, and aggregate table.
- [x] Add mocked agent/API tests that do not require a live API key.
- [x] Document startup order, secure key setup, endpoints, and tests.
- [x] Run full regression suite and live loopback dashboard/API health smoke test; record results. Full suite: 27 passed; compile, JavaScript syntax, and dependency checks passed; both local services healthy; OpenAI analysis correctly withheld because no newly rotated key is configured.

## Story Traceability
- **P3-US-1**: User asks a plain-language Gold question; agent discovers Phase 2 metadata and uses bounded aggregate queries.
- **P3-US-2**: User sees a concise response, insight, and one validated dynamic Vega-Lite chart.

## Constraints
- No direct Parquet/DuckDB access, arbitrary SQL, raw identifier dimensions, or row-level facts passed to OpenAI.
- Only Phase 2 documented joins are allowed; Phase 3 query results are capped at 200 rows (Phase 2 hard cap remains 500).
- Service binds to `127.0.0.1` only. LangGraph, Next.js, Cube, MCP, multi-widget canvas, and production authentication are deferred.
- The key pasted into chat is treated as exposed; it is not recorded or used. A newly rotated key must be configured locally.
