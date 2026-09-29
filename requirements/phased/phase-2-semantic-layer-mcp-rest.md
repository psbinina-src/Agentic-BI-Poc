# Phase 2: Local Gold Data REST API

## 1. Objective

Expose the existing Phase 1 Gold data model through a small, local, read-only REST API. The API provides catalogue discovery, dataset and field details, and bounded data access for a simple Phase 3 Agentic BI application. It does not create a separate semantic layer or redefine Gold measures.

## 2. Scope

This phase covers:

- catalogue discovery for the sales, customer, product, and inventory Gold datasets
- dataset grain, key, field name, type, and field description metadata
- a local REST API for validated, read-only dataset queries
- a stable JSON contract for Phase 3 agent/tool integration
- focused tests and simple local run instructions

Cube, MCP, SQL/BI connectivity, a second semantic model, authentication for remote use, and production hosting are out of scope. Any existing Cube prototype is not part of this API's runtime or data-access path.

### Local Runtime

Run the Python API as a native local process, bound to `127.0.0.1`. DuckDB reads the existing Gold Parquet files directly; Docker, Cube, WSL, external databases, and hosted services are not prerequisites.

## 2.1 Two-Developer Stories, Units, and Handoffs

| Story | User story outcome | Unit | Owner | Dependency / acceptance handoff |
|---|---|---|---|---|
| P2-US-1 | As an analytics consumer, I can discover the Gold datasets, their grains, keys, and fields. | P2-U1: Gold contract and catalogue metadata | One data engineer | Use the Phase 1 Gold contract; verify metadata against the Parquet schemas. |
| P2-US-2 | As a Phase 3 agent, I can retrieve bounded, validated data from Gold through a local REST interface. | P2-U2: Local Gold REST API | One data engineer | Query only the four allowlisted Gold datasets; verify filtering, grouping, aggregates, limits, and response shape. |

**Integration gate:** Validate catalogue and query responses against the actual Gold Parquet schemas and representative DuckDB results. Phase 3 consumes this documented local API contract.

## 3. Functional Requirements

### P2-FR-1: Gold Catalogue and Dataset Metadata

1. `GET /catalog` shall list the four Gold datasets, availability, descriptions, grains, key fields, and approved relationships.
2. `GET /catalog/{dataset}` shall return the dataset grain, key fields, and each physical field's name, DuckDB type, and description.
3. Field names and types shall be discovered from the Gold Parquet schema; catalogue descriptions shall explain the existing Phase 1 model without redefining its measures.

### P2-FR-2: Bounded Gold Data Access

1. `POST /query` shall read only the allowlisted Gold Parquet datasets and support field selection, validated filters, optional grouping, and basic field aggregations.
2. Query fields, grouping fields, filters, and aggregation inputs shall be checked against the selected dataset's physical schema.
3. Queries may join only relationships documented in the Gold catalogue; join keys and join types are fixed by the API, not supplied by the request.
4. Filter values shall be parameterized; request bodies shall not accept SQL text, file paths, database names, arbitrary table identifiers, or join expressions.
5. Query results shall default to 100 rows and have a hard maximum of 500 rows.
6. The API shall expose raw Gold fields and generic aggregations only; it shall not claim to provide governed business metric definitions.

### P2-FR-3: Local REST Contract

1. The API shall provide `GET /health`, `GET /catalog`, `GET /catalog/{dataset}`, and `POST /query` JSON endpoints.
2. The default server configuration shall bind to `127.0.0.1`; no remote exposure or firewall changes are allowed in this PoC.
3. API errors shall be structured and shall not expose local file paths or internal stack traces.
4. The API shall not send data to an external service. Phase 3 is responsible for selecting the minimum query result needed for any downstream model prompt.

## 4. Semantic Use Cases

The API supports Phase 3 discovery and retrieval over sales, customers, products, and inventory. Phase 3 chooses fields and filters, then interprets returned rows or generic grouped aggregates. Forecast data is not exposed unless present in the Gold model.

## 5. Acceptance Criteria

The phase is complete when:

1. all four Gold datasets appear in the catalogue with accurate grain, key, and relationship metadata
2. dataset detail endpoints expose actual Parquet field names and DuckDB types
3. bounded queries support projection, validated filters, grouping, and generic aggregates
4. invalid datasets, fields, unsafe request shapes, and excessive row limits are rejected
5. tests compare API results with direct DuckDB reads of synthetic Gold fixtures
6. the service starts locally on loopback and is documented for Phase 3 consumption

## 6. Deliverables

- local Gold catalogue and dataset schema endpoints
- bounded read-only data query endpoint
- API tests and Phase 3 integration contract
- local setup and run documentation
