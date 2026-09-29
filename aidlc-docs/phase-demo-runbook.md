# Agentic BI PoC — Phase Demo Runbook

This runbook is arranged for a screen recording: show the project status, open each phase summary, then run a representative command or dashboard for each phase. Run commands from the repository root in Windows PowerShell.

## Opening: Overall AI-DLC Status

Use [AI-DLC state](aidlc-state.md) for the current overall status. The short version:

| Phase | Status | Demo artifact |
|---|---|---|
| 1 — Lakehouse and Gold | Complete | Bronze/Silver/Gold validation and a direct Gold sales query |
| 2 — Gold REST API | Complete | Catalogue and bounded data query over Gold |
| 3 — Prompt-driven Agentic BI | Signed off with limitations | OpenAI-powered prompt dashboard calling Phase 2 |
| 4 — Static Gold dashboard | Signed off for implemented scope | Product Sales & Inventory Monitor |

Phase 3 caveat: six prompt/API calls returned successful aggregate results and chart specs. The low-stock suggestion fix is covered by tests, but its post-fix live prompt was not rerun. A full browser chart pass for all prompts was not performed.

---

## Phase 1 — Lakehouse and Gold Data Model

### Summary to show
Open [Phase 1 summary](phase-1/phase-1-summary.md) and [lakehouse README](../lakehouse/README.md).

### Validate the full pipeline

```powershell
py scripts/validate_phase1.py
```

This prints matching source/Bronze/Silver counts, Gold table counts, net sales, and low-stock totals. Existing verified Gold output includes 89,974 sales rows, 10,000 customers, 1,000 products, and 1,096,000 inventory snapshots.

### Show a direct Gold query result

```powershell
@'
import duckdb
con = duckdb.connect()
rows = con.execute("""
    SELECT channel,
           COUNT(DISTINCT order_id) AS completed_orders,
           ROUND(SUM(net_sales_amount), 2) AS net_sales
    FROM read_parquet('lakehouse/gold/sales_gold.parquet')
    GROUP BY channel
    ORDER BY net_sales DESC
""").fetchall()
print('Gold sales by channel')
print('channel | completed_orders | net_sales')
for row in rows:
    print(f'{row[0]} | {row[1]} | {row[2]}')
'@ | py -
```

Expected shape: Retail, Marketplace, and Online, with 14,997 completed orders per channel. Values are computed from the current generated Gold files and can change if data is regenerated.

---

## Phase 2 — Local Gold REST API

### Summary to show
Open [Phase 2 summary](phase-2/phase-2-summary.md). Phase 2 exposes the Gold catalogue, physical field metadata, approved relationships, and bounded read-only queries. It does not require Cube or MCP.

### Terminal 1: start the service

```powershell
py -m uvicorn p2_u2.api:app --app-dir src --host 127.0.0.1 --port 8100
```

Keep this terminal running. The API is loopback-only.

### Terminal 2: show catalogue and fields

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8100/health'
Invoke-RestMethod -Uri 'http://127.0.0.1:8100/catalog' | ConvertTo-Json -Depth 6
Invoke-RestMethod -Uri 'http://127.0.0.1:8100/catalog/sales_gold' | ConvertTo-Json -Depth 6
```

### Show data access: net sales by customer region

```powershell
$body = @{
  dataset = 'sales_gold'
  joins = @('customers_gold')
  group_by = @('customers_gold.region')
  aggregations = @(@{ field = 'sales_gold.net_sales_amount'; function = 'sum' })
  order_by = @(@{ field = 'customers_gold.region'; direction = 'asc' })
  limit = 20
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8100/query' -ContentType 'application/json' -Body $body | ConvertTo-Json -Depth 6
```

Expected: five regions. Stop Phase 2 with `Ctrl+C` after the later Phase 3 demo, since Phase 3 needs this service running.

---

## Phase 3 — Prompt-Driven Agentic BI

### Summary and tested prompts to show
Open [Phase 3 summary](phase-3/phase-3-summary.md) and [Phase 3 prompt test results](phase-3/phase-3-test-prompts.md). Six live prompts previously returned answer/insight/chart data:

1. `Show net sales by customer region`
2. `Show units sold by product category`
3. `What is the average discount rate by sales channel?`
4. `Compare average product-day stock coverage by product category.`
5. `Daily net sales by region during December 2025`
6. `Net sales by customer segment`

The low-stock dashboard suggestion is not in the verified list: its earlier live run failed; a fix is automated-test-covered but was not live-retested before sign-off.

### Key handling
The app reads `OPENAI_API_KEY` from the ignored root `.env` at startup. Do not show the key in the recording, terminal, API response, or source control. A key previously pasted into chat is exposed; rotate it when practical. The health endpoint reports only whether a key is configured.

### Terminal 1: start Phase 2 if not already running

```powershell
py -m uvicorn p2_u2.api:app --app-dir src --host 127.0.0.1 --port 8100
```

### Terminal 2: start the agent/dashboard

```powershell
py -m uvicorn p3_agent.api:app --app-dir src --host 127.0.0.1 --port 8200
```

Open `http://127.0.0.1:8200/`, enter a tested prompt, click **Analyze**, then show the answer, insight, Vega-Lite chart, and **View aggregated data**. Keep both services running during this segment. Stop each with `Ctrl+C` afterward.

---

## Phase 4 — Product Sales & Inventory Monitor

### Summary to show
Open [Phase 4 summary](phase-4/phase-4-summary.md) and [dashboard README](../dashboard/README.md). This is a static Gold-backed dashboard; it is independent of Phase 2/3 services. Metabase and semantic-SQL parity are deferred and are not part of the sign-off claim.

### Generate the current dashboard payload

```powershell
py -m p4_dashboard.generate
```

### Start the dashboard

```powershell
py -m http.server 8000 --directory dashboard
```

Open `http://127.0.0.1:8000/`. Show the Product Sales & Inventory Monitor, its KPI cards, Gold model view, charts, filters, sales trend, and inventory risk table. Stop with `Ctrl+C` when done.

---

## Final Automated Check (Optional)

```powershell
py -m pytest -q
```

Last recorded full-suite result: 30 passed. The Phase 3 limitations above remain part of the sign-off record.
