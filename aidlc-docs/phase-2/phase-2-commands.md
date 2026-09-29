# Phase 2 Commands — Local Gold REST API

The local REST API exposes only the Phase 1 Gold Parquet model for Phase 3 discovery and data access. It binds to loopback and does not require Node.js, Cube, MCP, Docker, WSL, credentials, or a hosted service.

## Prerequisites and Install

From the repository root, install project dependencies (including FastAPI/Uvicorn):

```powershell
py -m pip install -e ".[test]"
```

Gold data must exist under `lakehouse/gold/`. Rebuild it from Silver if needed:

```powershell
py -m p1_u4.cli --silver-dir lakehouse/silver --gold-dir lakehouse/gold
```

## Start the API

```powershell
py -m uvicorn p2_u2.api:app --app-dir src --host 127.0.0.1 --port 8100
```

Keep `--host 127.0.0.1`; do not bind to `0.0.0.0` or expose this PoC service remotely. Stop it with `Ctrl+C`.

To use a different Gold folder, set the environment variable before starting the server:

```powershell
$env:AGENTIC_BI_GOLD_DIR = "C:\path\to\gold"
py -m uvicorn p2_u2.api:app --app-dir src --host 127.0.0.1 --port 8100
```

## Discover Gold

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8100/health'
Invoke-RestMethod -Uri 'http://127.0.0.1:8100/catalog'
Invoke-RestMethod -Uri 'http://127.0.0.1:8100/catalog/sales_gold'
```

Catalogue entries include dataset description, grain, key fields, and availability. Dataset detail returns actual Parquet field names/types with descriptions. OpenAPI docs are available at `http://127.0.0.1:8100/docs` while the API is running.

## Query Gold for Phase 3

Example: Gold net sales by customer region, using the documented sales-to-customer relationship:

```powershell
$body = @{
	dataset = "sales_gold"
	joins = @("customers_gold")
	group_by = @("customers_gold.region")
	aggregations = @(@{ field = "sales_gold.net_sales_amount"; function = "sum" })
	order_by = @(@{ field = "customers_gold.region"; direction = "asc" })
	limit = 100
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8100/query' -ContentType 'application/json' -Body $body
```

The query endpoint supports projection or grouping/aggregations, filters (`eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `in`), sorting of selected output fields, and a default result limit of 100 (maximum 500). Joins must be selected from the catalogue's documented relationships; join keys/types are fixed. It rejects arbitrary SQL, unknown datasets/fields, unapproved joins, and client-supplied file paths. The API exposes raw Gold fields and generic aggregates, not a governed metric layer.

## Tests

```powershell
py -m pytest tests/p2_u2 -q
py -m pytest -q
```
