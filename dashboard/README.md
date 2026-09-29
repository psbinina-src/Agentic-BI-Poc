# Product Sales & Inventory Monitor

This lightweight static dashboard reads the Phase 1 Gold Parquet model and renders sales, customer, and inventory views without introducing a separate semantic layer. It serves as a traditional BI-style view alongside the Phase 3 prompt dashboard.

## Generate data

From the repository root:

```powershell
py -m p4_dashboard.generate
```

This writes `dashboard/data.json` based on the Gold tables:

- `sales_gold`
- `customers_gold`
- `products_gold`
- `inventory_gold`

The payload includes KPI summary values, a Gold model overview, revenue by region, sales by channel, a daily sales trend, inventory risk rows, and the date/product/customer filter values.

## Serve locally

From the repository root, start Python's static HTTP server:

```powershell
py -m http.server 8000 --directory dashboard
```

Then open:

```text
http://127.0.0.1:8000/
```

Use the date range, product, and customer controls to filter the sales KPIs/charts; **Reset** restores the complete Gold range. The sales trend aggregates actual `sales_gold.order_date` values. Stop the server with `Ctrl+C`.

## Tests

```powershell
py -m pytest tests/test_phase4_dashboard.py -q
py -m pytest -q
```

## Scope Note

The original Phase 4 requirement described Metabase connected to a Phase 2 semantic SQL endpoint. The implemented PoC instead uses a standalone static dashboard directly over the Phase 1 Gold outputs. Cube/Metabase, semantic SQL, and cross-interface metric parity are not implemented in this Phase 4 slice. Dashboard calculations are independently based on the Gold rows.
