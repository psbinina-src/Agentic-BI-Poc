# Local Lakehouse

This directory is the local Phase 1 lakehouse for the project.

## Layer layout
- `source/` — generated synthetic source CSVs and manifest
- `bronze/` — raw accepted Parquet outputs
- `silver/` — typed and quality-checked Silver outputs
- `gold/` — business-ready Gold outputs and sample query evidence

## Contract
- Source files are generated under `lakehouse/source/`.
- Bronze must be written under `lakehouse/bronze/`.
- Silver must be written under `lakehouse/silver/`.
- Gold must be written under `lakehouse/gold/`.

This is the official local-first storage layout for the Phase 1 implementation.
