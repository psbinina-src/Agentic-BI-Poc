# P2-U2 Business Rules — Local Gold REST API

1. The API exposes only the four Phase 1 Gold datasets; it does not scan Silver/Bronze/source files or other filesystem locations.
2. The catalogue reports the existing Gold grains and keys; field names and types come from the actual Parquet schemas.
3. The catalogue reports only fixed Gold model relationships: sales to customers/products, and inventory to products. Joins are left joins using the documented keys.
4. The API returns Gold fields and generic aggregates only. It does not create a separate semantic model or redefine business metric formulas.
5. Query dataset, join, projection, grouping, filter, aggregation, and sort fields must match documented relationships, physical schemas, or output aliases.
6. Filter values are always passed as parameters. The API rejects SQL text, arbitrary table names, file paths, unknown fields, and malformed filter values.
7. The API is read-only, defaults to 100 result rows, and rejects limits above 500.
8. Only `127.0.0.1` is an approved listen address; do not add CORS, remote access, firewall changes, or public deployment in this PoC.
9. Missing Gold datasets return a concise not-found response. Invalid requests return structured errors without local paths or stack traces.
10. Date values are returned in ISO format; decimals are emitted as JSON numeric values.
11. Phase 3 is responsible for interpreting the exposed Gold fields and selecting the minimum result data needed for model prompts. No data is sent externally by this API.
