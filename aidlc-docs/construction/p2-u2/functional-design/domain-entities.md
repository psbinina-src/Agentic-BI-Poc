# P2-U2 Domain Entities — Local Gold REST API

## Gold Dataset
 - **Identity**: One of `sales_gold`, `customers_gold`, `products_gold`, or `inventory_gold`.
 - **Attributes**: Description, row grain, key fields, availability, and physical fields.
 - **Source**: The matching allowlisted Parquet file under the configured Gold directory.
- **Relationships**: Fixed joins between sales and customer/product dimensions, and inventory and product dimension.

## Gold Field
 - **Attributes**: Physical field name, DuckDB Parquet type, and concise field description.
 - **Source**: Field names/types are inspected from the Parquet schema; descriptions document the Phase 1 Gold contract.

## Data Query
- **Inputs**: Dataset name, optional documented dimension joins, projected fields OR grouping and generic aggregations, optional field filters/order, and result limit.
- **Validation**: Dataset/field allowlists derive from the Gold schema; joins use only documented keys; filter values are bound parameters; SQL text and paths are not accepted.
 - **Bounds**: Default 100 rows, maximum 500; grouping and aggregation requests are also capped in number of fields.

## Query Result
 - **Fields**: Dataset name, output columns, JSON rows, row count, applied limit, and truncation flag.
 - **Origin**: Direct read-only DuckDB query over the selected Gold Parquet file. The API does not define business metrics.

## REST Endpoints
 - `GET /health`: local API and available Gold dataset status.
 - `GET /catalog`: dataset names, descriptions, grains, keys, and availability.
 - `GET /catalog/{dataset}`: physical fields, DuckDB types, and descriptions.
 - `POST /query`: bounded data access for Phase 3.
