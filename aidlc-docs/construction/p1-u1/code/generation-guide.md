# P1-U1 Synthetic Source Generator — Local Guide

## Prerequisites
- Python 3.11 or newer. The development workspace was checked with Python 3.14.4.
- Windows PowerShell or another terminal at the repository root.
- Internet access is needed only if installing the package/test dependency; generation itself makes no network calls.

## Install and Test
Create/use a local virtual environment if desired, then install the source package in editable mode with test tools:

```powershell
python -m pip install -e ".[test]"
python -m pytest
```

## Generate the Default Dataset
From the repository root:

```powershell
python -m p1_u1
```

The default settings are loaded from [p1-u1-defaults.toml](../../../../config/p1-u1-defaults.toml): seed `42`, inclusive dates `2023-01-01` to `2025-12-31`, 10,000 customers, 1,000 products, 100,000 order lines, and output directory `lakehouse/source/`.

## Override Settings
CLI options override TOML settings. Example with a small local development dataset:

```powershell
python -m p1_u1 --seed 7 --start-date 2024-01-01 --end-date 2024-03-31 --customers 100 --products 30 --order-lines 500 --output-dir lakehouse/source
```

Use `python -m p1_u1 --help` for the available options. Dates are inclusive ISO dates. Counts must be positive integers.

## Outputs
A successful run writes these UTF-8 CSV files and then `manifest.json` under the configured output directory:

- `customers.csv`
- `products.csv`
- `orders.csv`
- `order_lines.csv`
- `inventory_snapshots.csv`
- `manifest.json` — effective settings, schema version, counts, output paths, checksums, source validation/scenario results, and run timestamp.

The manifest is the success marker. Downstream Bronze ingestion must not consume source files unless a valid manifest is present and the listed files/checksums match. If a run fails while writing, direct-path partial files may remain without a manifest. Fix the cause and rerun; there is no automatic retry, rollback, backup, or prior-run preservation guarantee.

## Reproducibility and Scenarios
Same generator version, seed, effective dates, and sizes reproduce the same logical entity rows and canonical CSV checksums. The operational manifest timestamp differs by run. Generated scenarios include repeat buyers, temporal/region/category variation, and products with completed-order sales and low-stock inventory snapshots. Customer labels are synthetic placeholders only.

## Size and Runtime Notes
At defaults, the inventory snapshots alone contain 1,096,000 rows because the date range includes leap day 2024. The approved design constructs complete entity collections in memory before validation and writing; memory use grows with configured volume and no maximum size or hard runtime/memory target is promised. The run summary reports elapsed seconds and entity row counts as informational evidence.

Generated datasets under `lakehouse/` are ignored by Git. Do not commit generated data; schemas and instructions are maintained in documentation.
