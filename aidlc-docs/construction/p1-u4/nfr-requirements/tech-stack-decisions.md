# P1-U4 Tech Stack Decisions — Gold Models, Samples, and Phase 2 Handoff

## Chosen Stack
- Python + DuckDB for local Gold transformation and sample query execution
- Parquet outputs for Gold data stores
- Local files for sample query evidence and handoff documentation

## Rationale
This final Gold unit stays within the same local-first design as the previous Phase 1 units. It avoids infrastructure complexity while producing a business-ready output that downstream semantic modeling can consume.

## Acceptance fit
The stack keeps all outputs inspectable and reproducible while preserving the project’s local-first architecture and the approved Phase 1 contract.
