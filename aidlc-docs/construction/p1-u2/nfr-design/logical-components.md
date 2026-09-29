# P1-U2 Logical Components — Bronze Ingestion and Lineage

## Component Inventory

### 1. Manifest Validation Component
Responsible for:
- verifying the source manifest exists
- confirming it is valid JSON
- checking required fields are present
- ensuring `validation.passed` is true

Outputs:
- accept or reject source run
- structured error messages for invalid or missing source metadata

### 2. Source Integrity Component
Responsible for:
- verifying the five expected source documents are present
- computing and comparing SHA-256 hashes
- confirming run-to-file integrity before publication

Outputs:
- source-check status
- failing entity name and mismatch details

### 3. CSV Ingestion Component
Responsible for:
- reading each approved CSV file with DuckDB
- preserving the source row values without business transformation
- preparing the raw table for Bronze writing

Outputs:
- raw entity relation ready for Parquet conversion

### 4. Lineage Metadata Component
Responsible for:
- appending `source_file`, `source_row_number`, `source_run_id`, and `ingested_at`
- preserving row identity for later debugging and lineage inspection

Outputs:
- Bronze row set with explicit run provenance

### 5. Bronze Output Component
Responsible for:
- writing clean Parquet files under the Bronze path
- storing each entity as a direct raw representation of the accepted source

Outputs:
- Bronze Parquet files and a corresponding load status record

### 6. Failure Reporting Component
Responsible for:
- raising or returning actionable errors for parse failures, mismatches, missing files, and invalid manifests
- preventing downstream stage consumption of invalid data

Outputs:
- structured runtime error details and no success marker for failed runs

## Interactions
The components are linear and ordered by dependency:
1. Validate manifest
2. Validate files and checksums
3. Ingest CSV to raw Bronze relation
4. Attach lineage metadata
5. Write Parquet outputs
6. Report success or fail

This ordering ensures the Bronze layer stays deterministic and safe for P1-U3 and P1-U4 downstream use.
