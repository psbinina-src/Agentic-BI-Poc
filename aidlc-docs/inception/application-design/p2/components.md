# Phase 2 Components

## 1. Gold Contract
- **Purpose**: Supply the Phase 2 semantic layer with stable, local Gold Parquet datasets and documented grains, keys, and metric inputs.
- **Responsibility**: P2-U1 verifies/corrects completed-order sales and inventory demand/coverage inputs before Cube model work depends on them.
- **Interface**: Existing `lakehouse/gold/*.parquet` files plus schema/grain/formula handoff and representative expected query results.

## 2. Cube Core Semantic Service
- **Purpose**: Be the single canonical definition of business measures, dimensions, joins, and filters.
- **Responsibility**: Read the configured local Gold data using DuckDB, publish the Cube model/catalog, and serve REST and Postgres-protocol SQL APIs.
- **Interface**: Local REST metadata/load endpoints and SQL API, with the SQL port explicitly enabled.
- **Constraint**: Native host process only, bound to loopback for the PoC. Prove Cube Core and the DuckDB driver can run against the Gold Parquet path without Docker before the service work proceeds.

## 3. Local MCP Adapter
- **Purpose**: Provide the required local MCP protocol interface without depending on Cube's hosted MCP connector.
- **Responsibility**: Expose a small read-only tool set for catalog discovery and governed metric queries; translate requests to Cube REST metadata/load calls.
- **Interface**: Local MCP stdio process using the Python MCP SDK; only allowlisted semantic member names, filters, and bounded result sizes are accepted. No arbitrary SQL or direct lakehouse query path.
- **Dependency**: P2-U2 only; Cube remains the metric authority.

## 4. Analytics and Agent Consumers
- **Purpose**: Consume the governed semantic catalog and results.
- **Interfaces**: Cube REST for applications, Cube SQL API for SQL-compatible BI validation, and the local MCP adapter for MCP clients.

## Unit Ownership
- **P2-U1**: Gold contract, Cube model, catalog metadata, and representative expected results.
- **P2-U2**: Native service wiring, local MCP adapter, SQL access configuration, integration/parity tests, and setup examples. Start only after the P2-U1 handoff passes.
- **Owner**: One data engineer; work is sequential, not parallel.
