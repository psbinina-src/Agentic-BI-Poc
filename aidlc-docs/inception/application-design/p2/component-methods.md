# Phase 2 Component Interfaces

High-level interface sketches only; business formulas and detailed validation rules belong in per-unit Functional Design.

## Gold Contract
- `inspect_gold_contract(gold_path) -> GoldContract`: Return available datasets, columns, grains, and key candidates for review.
- `build_or_correct_gold(config) -> GoldHandoff`: Produce or verify accepted sales and inventory inputs; return schemas, quality status, and sample expected results.

## Cube Core Semantic Service
- `load_catalog() -> CatalogMetadata`: Return discoverable semantic views, measures, dimensions, and descriptions from Cube metadata.
- `query_metrics(query: GovernedQuery) -> QueryResult`: Execute a bounded Cube REST load query using validated semantic member names.
- `execute_sql(sql: str) -> SqlResult`: Submit a BI validation query through Cube's Postgres-protocol SQL API; enabled only after local credentials/config are set.

## Local MCP Adapter
- `list_catalog(search: str | None) -> CatalogPage`: Find Cube semantic views and members and return compact descriptions.
- `run_metric_query(measures, dimensions, filters, time_dimensions, limit) -> QueryResult`: Validate an allowlisted Cube query shape, then call Cube REST. Arbitrary SQL is not an input.
- `serve_stdio() -> None`: Start the local MCP process for an MCP client using stdio transport.

## Contract Types
- `GoldContract`: Local Gold path, dataset schemas, grains, keys, and semantic mapping evidence.
- `CatalogMetadata`: Cube member IDs, display names, types, descriptions, and allowed member sets.
- `GovernedQuery`: Requested measures/dimensions, supported filters/date range, and bounded limit.
- `QueryResult`: Column metadata and rows returned by Cube.
- `GoldHandoff`: Pass/fail status, versioned schema/formula notes, and representative expected results.
