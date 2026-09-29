# Phase 3 Summary — Prompt-Driven Gold Data Intelligence

## Purpose
Phase 3 provides a simple prompt dashboard for sales, customer, product, and inventory analysis. A local Python agent uses OpenAI tool calling to inspect Phase 2 Gold catalogue metadata and request bounded aggregated data only through the Phase 2 REST API. It returns a concise answer, an insight, and a field-validated Vega-Lite chart.

## Scope
- One Python FastAPI service hosts both the prompt endpoint and static dashboard.
- The browser submits natural-language questions to `POST /api/ask`.
- The agent discovers and queries Gold via `PHASE2_API_URL` (default `http://127.0.0.1:8100`).
- The LLM receives aggregate query results, not row-level customer/product records.
- Vega-Lite specifications are restricted to safe marks/channels and fields returned by Phase 2.
- The Phase 3 server binds to `127.0.0.1`; no credentials are returned to the browser.

Deferred to keep the PoC simple: LangGraph, Next.js, Cube, MCP, cross-interface governance, multi-widget canvases, user-managed layouts, and production authentication/hosting. Forecasts are not fabricated when no forecast Gold dataset exists.

## Local Start
1. Follow the two-terminal startup and local `.env` configuration in [Phase 3 commands](phase-3-commands.md).
2. Start Phase 2 first on `127.0.0.1:8100`, then Phase 3 on `127.0.0.1:8200`.
3. Open `http://127.0.0.1:8200/`; stop both services with `Ctrl+C` when done.

## Data Flow
`Browser question -> Phase 3 API -> OpenAI tool call -> Phase 2 catalogue/query API -> aggregated Gold rows -> validated Vega-Lite + insight -> Browser`

The Phase 3 agent does not read Parquet or execute SQL directly. OpenAI inference needs internet access. Only aggregate results are sent to OpenAI; use synthetic/non-sensitive Gold data for this PoC.

## Verification and Sign-Off Checklist
- Focused Phase 3 suite: `py -m pytest tests/p3 -q` — **10 passed**.
- Full project suite: `py -m pytest -q` — **30 passed**.
- Python compile, dashboard JavaScript syntax, and dependency checks passed.
- Six live Phase 3 prompt/API runs returned validated chart specs and aggregate data; see [Phase 3 prompt test results](phase-3-test-prompts.md).
- Five matching Gold query shapes returned HTTP 200 against the live Phase 2 API.
- **Known limitation accepted at sign-off:** the low-stock dashboard suggestion failed in its live run before the base-key count fix. The fix is covered by automated tests, but no post-fix live rerun was performed. The full browser chart-rendering pass for every prompt was also not performed.
- The OpenAI key is read from ignored `.env`; it was exposed in chat and is being used only because the user explicitly approved it for this synthetic-data PoC. Rotate before any reuse beyond this PoC.

## Phase 3 Sign-Off
Phase 3 is closed for the current PoC scope using the evidence above, at the user's direction not to perform further testing. Six prompts have live successes; the low-stock prompt's post-fix behavior remains unverified and is explicitly not counted as a passing live test. Further development/testing is deferred unless requested.
