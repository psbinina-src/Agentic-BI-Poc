# Integration Test Instructions — Phase 2 Gold REST API

## Purpose
Verify the local REST service reads the real Gold Parquet files and exposes the Phase 3 data contract over HTTP.

## Start the Service
From the repository root, start the server in one PowerShell terminal:

```powershell
py -m uvicorn p2_u2.api:app --app-dir src --host 127.0.0.1 --port 8100
```

Keep the loopback bind and leave the server running while checking the endpoints from another terminal.

## Smoke Test Catalogue and Schema

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8100/health'
Invoke-RestMethod -Uri 'http://127.0.0.1:8100/catalog'
Invoke-RestMethod -Uri 'http://127.0.0.1:8100/catalog/sales_gold'
```

Expected: health reports four available datasets; catalogue contains the four Gold datasets and fixed relationships; sales details include physical field names/types.

## Smoke Test Joined Data Access

```powershell
$body = @{
  dataset = "sales_gold"
  joins = @("customers_gold")
  group_by = @("customers_gold.region")
  aggregations = @(@{ field = "sales_gold.net_sales_amount"; function = "sum" })
  order_by = @(@{ field = "customers_gold.region"; direction = "asc" })
  limit = 10
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8100/query' -ContentType 'application/json' -Body $body
```

Expected: five regional groups from the current Gold dataset, with no more than 10 rows. Stop the service with `Ctrl+C` after verification.
