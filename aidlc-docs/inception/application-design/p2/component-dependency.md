# Phase 2 Component Dependencies

| Consumer / component | Depends on | Communication | Gate |
|---|---|---|---|
| Cube Core Semantic Service | Gold Contract | DuckDB reads local Gold Parquet; Cube model maps governed members | Gold schemas, grains, and formulas reviewed in P2-U1 |
| REST consumers | Cube Core Semantic Service | Local Cube REST metadata and load APIs | Model compiles and representative queries pass |
| SQL/BI consumers | Cube Core Semantic Service | Local Cube Postgres-protocol SQL API | SQL API explicitly enabled and tested against the model |
| Local MCP Adapter | Cube Core Semantic Service | Local Cube REST metadata/load APIs | Only allowlisted, bounded semantic queries pass validation |
| MCP clients | Local MCP Adapter | MCP stdio transport | Local client connection and representative tools verified |

## Data and Control Flow

Gold Parquet -> DuckDB source access -> Cube semantic model -> Cube REST and SQL APIs

MCP client -> local Python MCP adapter -> validated Cube REST request -> Cube semantic model

## Dependency Rules
- REST, SQL, and MCP are consumers of one Cube model; they do not contain independent business formulas.
- The MCP adapter cannot read Gold Parquet directly and cannot submit arbitrary SQL.
- P2-U2 interface work is blocked until P2-U1 publishes a passing Gold/semantic contract and representative expected results.
- If local native Cube Core with DuckDB cannot be demonstrated without a container runtime, stop before adding an alternate platform or hosted dependency.
