# Phase 1 Summary — Lakehouse Implementation and Available Outputs

## Overview
Phase 1 implements a local-first lakehouse pattern using a deterministic source dataset, then progressively layering Bronze, Silver, and Gold outputs on top of the source data.

The pipeline is:

source -> bronze -> silver -> gold

This is built for a local PoC workflow and is intentionally simple: no external services, no container dependency, and no distributed runtime.

## How the lakehouse is implemented

### 1. Source layer
The source dataset is generated in `lakehouse/source/`.

Files created:
- `customers.csv`
- `products.csv`
- `orders.csv`
- `order_lines.csv`
- `inventory_snapshots.csv`
- `manifest.json`

This layer acts as the source-of-truth input contract. A manifest records checksums, validation status, and the expected dataset shape.

### 2. Bronze layer
The Bronze layer is the raw ingest layer under `lakehouse/bronze/`.

Bronze purpose:
- preserve raw values from the source files
- retain lineage metadata
- validate file-level checksum and source completeness before ingestion

Bronze files available:
- `customers.parquet`
- `products.parquet`
- `orders.parquet`
- `order_lines.parquet`
- `inventory_snapshots.parquet`

Bronze includes lineage fields such as:
- `source_file`
- `source_row_number`
- `source_run_id`
- `ingested_at`

### 3. Silver layer
The Silver layer is under `lakehouse/silver/`.

Silver purpose:
- standardize raw values into typed columns
- enforce quality rules on required fields, duplicates, nulls, and domain expectations
- keep lineage available for traceability

Silver files available:
- `customers.parquet`
- `products.parquet`
- `orders.parquet`
- `order_lines.parquet`
- `inventory_snapshots.parquet`
- `silver_quality_report.json`

This is the first quality-checked business layer. It is the bridge between raw ingestion and analytical modeling.

### 4. Gold layer
The Gold layer is under `lakehouse/gold/`.

Gold purpose:
- build business-ready analytical tables
- expose sales and inventory facts
- provide customer and product dimensions for downstream BI or semantic modeling

Gold files available:
- `sales_gold.parquet`
- `customers_gold.parquet`
- `products_gold.parquet`
- `inventory_gold.parquet`

## Current dimensional model
The implemented Phase 1 model is a lightweight star schema:

- Sales fact: `sales_gold.parquet`
  - grain: order line
  - measures: gross sales, discount, net sales
- Customer dimension: `customers_gold.parquet`
- Product dimension: `products_gold.parquet`
- Inventory fact: `inventory_gold.parquet`
  - grain: product-day snapshot
  - measures: inventory levels and low-stock signals

The current model does not include a separate date dimension table. Date semantics are carried directly in the fact tables using `order_date` and `snapshot_date` fields. This is the validated Phase 1 implementation.

## What is available today

### Available source data
- deterministic synthetic customer, product, order, order-line, and inventory snapshot data
- manifest proving the source contract and file checksums

### Available Bronze data
- raw ingested data from the source files
- lineage metadata captured for each row

### Available Silver data
- typed and quality-checked business data
- explicit quality report for review and governance

### Available Gold data
- analytical fact and dimension outputs ready for BI or semantic-layer consumption
- sample query outputs and business-ready metrics derived from accepted Silver data

## Validation status
The Phase 1 implementation has been executed successfully in this workspace and validated by the project test suite and a direct Python DuckDB validation script.

The current validation command is:

```powershell
python scripts/validate_phase1.py
```

This confirms the populated lakehouse is consistent with the intended source -> bronze -> silver -> gold flow.
