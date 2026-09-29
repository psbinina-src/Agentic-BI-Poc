# P1-U2 Business Rules — Bronze Ingestion and Lineage

## Rule Set
1. Source acceptance rule: A source run is valid only if the U1 manifest exists, is parseable, has `validation.passed == true`, all expected files exist, and each file checksum matches the recorded value.
2. File-discovery rule: U2 reads exactly the five source entities expected by the manifest: customers, products, orders, order_lines, inventory_snapshots.
3. Raw-preservation rule: Bronze writes the source data as-is to Parquet; only lineage metadata is appended. No business transformation, null repair, or type inference occurs in U2.
4. Data-grain rule: Each Bronze dataset retains the original row grain, and each row includes `source_file`, `source_row_number`, `source_run_id`, and `ingested_at`.
5. Load-atomicity rule: If any source validation step fails, there is no successful Bronze load marker and no downstream Bronze dataset is considered accepted.
6. Traceability rule: Source lineage must be inspectable by file name, run ID, and row number to support downstream debugging and quality analysis.
7. Location rule: Bronze output path(s) and load metadata must be written to the configured `lakehouse/bronze/` area and captured in the load manifest for downstream stages.
8. Repeatability rule: Re-running the same accepted source manifest should yield the same Bronze row set and the same per-row lineage metadata, except for `ingested_at` and the run manifest timestamp.
9. Fail-fast rule: File parse errors, output write failures, or checksum mismatch problems terminate with actionable diagnostics and do not publish a positive Bronze status.
10. Handoff rule: P1-U3 uses only accepted Bronze outputs and their run metadata; it does not consume partial or unmanifested ingest results.

## Validation and Decision Outcomes
- Source manifest check is mandatory before any Bronze output is written.
- File checksum mismatch is a blocking error; no source data is accepted into Bronze.
- A parse failure or unsupported source file format is a blocking error.
- Missing or invalid source file name in the manifest is a blocking error.
- Bronze load metadata reflects both the run-level load manifest and the row-level lineage fields.

## Non-Goals
- Silver-type conversion, null handling, and business transformations are outside U2 scope.
- Data quality checks beyond source integrity are deferred to U2 validation and then later to P1-U3.
- U2 does not use the external LLM, web service, or container runtime; it stays local-first and file-driven.
