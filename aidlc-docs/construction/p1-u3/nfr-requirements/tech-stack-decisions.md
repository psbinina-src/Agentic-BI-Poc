# P1-U3 Tech Stack Decisions — Silver Standardization and Data Quality

## Chosen Stack
- Python for orchestration and validation logic
- DuckDB for local SQL-based transformation and data-quality filtering
- Parquet for Silver persistent output
- Local file system for intermediate and final evidence/reporting

## Rationale
This unit continues the local-first design from P1-U2 and adds typed data standardization with explicit pass/fail quality gates. The stack preserves determinism and keeps the overall Phase 1 pipeline simple and inspectable.

## Design Decisions
- Source-of-truth ordering: Bronze is read-only, Silver is typed and standardized, Gold is business-ready.
- Quality checks run before accepting Silver output for downstream consumption.
- The quality report is persisted as an explicit artifact to support auditability and future review.
- No network or container dependency is added.

## Acceptance Fit
This stack supports the approved P1-U3 design and keeps the code easy to test locally while preserving the overall lakehouse architecture without external complexity.
