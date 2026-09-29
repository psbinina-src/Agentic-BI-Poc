# Phase 4 Summary — Product Sales & Inventory Monitor

## Outcome
A static local dashboard presents Gold sales, customer, product, and inventory views. The dashboard is generated from `lakehouse/gold/*.parquet` into a local `dashboard/data.json` payload and served by Python's standard HTTP server.

## Dashboard Contents
- Net sales, gross sales, units sold, completed orders, and average order value KPIs.
- Gold table/field semantic-view cards.
- Revenue by customer region and sales by channel.
- Daily sales trend aggregated from actual Gold `order_date` values.
- Inventory risk table with on-hand quantity, sales velocity, coverage, and stock status.
- Date range, product, and customer filters for the sales result views, plus a reset control.

## Generate and Start
Run from the repository root in PowerShell:

```powershell
py -m p4_dashboard.generate
py -m http.server 8000 --directory dashboard
```

Open `http://127.0.0.1:8000/`. Stop the server with `Ctrl+C`. Gold Parquet data must already exist under `lakehouse/gold/`.

Detailed instructions: [Dashboard README](../../dashboard/README.md).
The ordered Phase 1–4 recording sequence is in the [phase demo runbook](../phase-demo-runbook.md).

## Validation
- Focused Phase 4 test: `py -m pytest tests/test_phase4_dashboard.py -q`.
- Full project suite: `py -m pytest -q`.
- The contract test verifies summary values, Gold semantic-view presence, regional/channel series, and inventory-risk rows.

## Scope and Known Limitations
- This implementation is a standalone static dashboard directly over Gold Parquet outputs.
- It does not require Phase 2 REST or Cube at runtime and is not connected to Metabase.
- The earlier Metabase/semantic-SQL parity requirements are deferred; no cross-interface parity claim is made.
- Sales filters are applied in the dashboard payload's sales rows. Inventory remains a separate current Gold risk snapshot and is not recomputed under sales filters.
- The dashboard uses synthetic local data only and is not a production-hosted service.

## Sign-Off
Phase 4 is signed off for the implemented static Gold dashboard scope. The known deviation from the original Metabase/semantic-SQL requirement is explicit above and in the dashboard README.
