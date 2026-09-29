# P2-U2 Business Logic Model — Local Gold REST API

## Purpose
Expose the Phase 1 Gold Parquet model through a small local REST API. The API supplies catalogue metadata and bounded read-only data queries to Phase 3; it does not define new business metrics.

## Query Flow
1. `GET /health` reports API status and number of available Gold datasets.
2. `GET /catalog` lists the four dataset contracts: names, descriptions, grains, key fields, availability, and documented relationships.
3. `GET /catalog/{dataset}` inspects the physical Parquet schema and combines each field's name/type with its field description.
4. `POST /query` validates a dataset and field selection or grouping/aggregation, builds a parameterized DuckDB read over Gold Parquet, and returns JSON rows. Only documented relationship joins can be selected; keys and join types are fixed.
5. The default query limit is 100 and the hard maximum is 500. Invalid datasets/fields, unsupported request shapes, SQL strings, client paths, and unapproved joins are rejected.

Phase 3 discovers metadata first, then requests only the Gold fields and row scope needed for the question. Date fields serialize as ISO strings; decimal results serialize as JSON numbers. The API does not send data to a model or calculate new business metrics.
