# Phase 2 Story-to-Unit Map

| Story | Outcome | Primary unit | Coverage / acceptance handoff |
|---|---|---|---|
| P2-US-1 | Analytics consumers discover governed metrics and dimensions over Gold. | P2-U1 — Gold Contract and Semantic Catalog | Stable Cube model/catalog; Gold grains, keys, formulas, and names documented; metadata discovery and representative metric queries verified. |
| P2-US-2 | Agents and BI consumers access the same governed metrics through supported interfaces. | P2-U2 — Local Interfaces and Parity | Local REST, SQL-compatible, and MCP paths use Cube definitions; equivalent requests match P2-U1 expected results; endpoint/setup examples published. |

## Shared Constraints
- One data engineer owns both stories and units sequentially.
- P2-U2 is blocked by P2-U1's Gold, semantic-name, native-runtime, and expected-result handoff.
- Forecast measures remain out of scope until forecast Gold data is available.
- Parity validation belongs to P2-U2 and is not a standalone unit/story.
