# P1-U2 Business Logic Model — Bronze Ingestion and Lineage

## Purpose
P1-U2 accepts only the approved P1-U1 source contract and loads the raw CSV content into Bronze Parquet with minimal transformation and strict lineage. Bronze is explicitly raw and preserves source values; data typing and business transformation are deferred to Silver.

## Business Context
The process starts from a valid P1-U1 source run: five canonical CSV files and a manifest, all under the repository-local `lakehouse/source/` path. The Bronze ingestion job verifies the manifest, checks output file integrity, checks file presence, and then loads each entity into a Bronze dataset with hidden lineage metadata so later stages can trace data to its source run.

## Core Business Flow
1. Preflight the source manifest.
   - Manifest exists and is parseable.
   - `validation.passed` is true.
   - All expected entity files exist.
   - Each file matches its recorded SHA-256 checksum.
   - Counts in the manifest match the actual loaded entity files.
2. Load source entity files to Bronze tables.
   - Each table preserves the source column names and the source row content as raw strings.
   - The ingest job reads the full file into Parquet without business transformation.
3. Enrich each written row with ingestion lineage metadata.
   - `source_file`
   - `source_row_number`
   - `ingested_at`
   - `source_run_id`
4. Publish Bronze dataset status metadata.
   - Output path(s)
   - Source manifest reference
   - Total row counts
   - Validation and checksum status
   - Result status: success or failed
5. Stop before dependent stages if any contract or integrity check fails.

## Data Model and Grain
Each row in Bronze is a direct raw representation of the source row with lineage columns appended. The primary grain is the source row grain for each source file.

### Bronze entity mapping
- `customers_bronze`: one row per source customer row, raw columns preserved, plus lineage metadata.
- `products_bronze`: one row per source product row, raw columns preserved, plus lineage metadata.
- `orders_bronze`: one row per source order row, raw columns preserved, plus lineage metadata.
- `order_lines_bronze`: one row per source order-line row, raw columns preserved, plus lineage metadata.
- `inventory_snapshots_bronze`: one row per source inventory row, raw columns preserved, plus lineage metadata.

### Lineage metadata
Each Bronze table adds the following fields:
- `source_file` — the source CSV name
- `source_row_number` — the original row number within the file
- `source_run_id` — stable identifier drawn from the source manifest or generated manifest timestamp/checksum fingerprint
- `ingested_at` — UTC timestamp when the row was loaded into Bronze

This metadata is not a business transformation; it is a traceability layer required for later lineage inspection and debugging.

## Rules and Decision Logic
- The Bronze ingestion run is atomic at the U2 layer: if any expected source entity or manifest check fails, the whole Bronze ingestion operation is reported as failed and no successful Bronze load manifest is published.
- A successful Bronze run only writes output after all source checks pass.
- The source manifest and file checksum contract from P1-U1 is authoritative. Checksum mismatches are treated as a hard failure.
- Data is stored with raw string values and source-defined values; Bronze does not apply semantic validation or business rules beyond source adoption and lineage tagging.
- Bronze is the raw starting layer; Silver is responsible for typed dimensions, standardization, and data quality corrections.

## Error Handling and Failure Conditions
A Bronze load fails when any of the following happens:
- Manifest is missing, invalid, or unparsable.
- `validation.passed` is false.
- Any expected source file is missing.
- Any file checksum mismatch occurs.
- Any CSV cannot be parsed to the expected entities.
- Any output path cannot be created or written.

Failed operations must return actionable diagnostics and must not create a success manifest for Bronze. Downstream stages must not consume unaccepted Bronze data.

## Traceability Value
Bronze provides a recoverable raw history of each source run. This allows later issues to be traced back to:
- source manifest/session
- source generator version/seed/date range/volume
- source file and row number
- ingest timestamp and run ID

This is the required foundation for later Silver and Gold quality checks.
