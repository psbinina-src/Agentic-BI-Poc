# Phase 1 Story and Requirement to Unit Map

## Story-to-Unit Mapping

| Story | User outcome | Assigned unit(s) | Ownership and sequence |
|---|---|---|---|
| P1-US-1 | Reproducibly generate synthetic source data and load stable, traceable Bronze inputs | P1-U1 generator/source contract -> P1-U2 Bronze ingestion/lineage | One data engineer owns both; U2 begins after U1's source contract and reproducibility evidence pass |
| P1-US-2 | Provide clean, documented Gold models for sales, customer, and inventory analysis | P1-U3 Silver standardization/quality -> P1-U4 Gold models, sample queries, Phase 2 handoff | Same data engineer owns both; U3 begins after U2's Bronze handoff and U4 after U3's Silver handoff |

## Requirement-to-Unit Coverage

| Requirement area | P1-U1 | P1-U2 | P1-U3 | P1-U4 |
|---|---|---|---|---|
| Synthetic generation, deterministic seed/configuration, entity scenarios, source CSV schemas | Primary | Consumes source contract |  |  |
| Bronze ingestion, raw values, load metadata, reload/lineage | Handoff source | Primary | Consumes Bronze contract |  |
| Silver standardization, type conversion, invalid/null/duplicate rules |  | Provides Bronze inputs | Primary | Consumes Silver contract |
| Gold facts/dimensions for sales and customer analysis |  |  | Provides standardized inputs | Primary |
| Gold inventory, stock health/velocity, baseline forecast |  |  | Provides standardized inputs | Primary |
| Sample queries, documentation, quality evidence, end-to-end acceptance | Generation evidence | Bronze evidence | Quality and Silver evidence | Integrated evidence and final handoff |
| Stable Gold contract for Phase 2 semantic modeling |  |  |  | Primary |

## Traceability to Approved Requirements

The clarified requirements artifact numbers its requirements differently from the original phase specification. The tables below name the source explicitly to avoid confusing similarly numbered requirements.

### Clarified `aidlc-docs/inception/requirements/requirements.md`

| Requirement ID/area | Coverage |
|---|---|
| P1-FR-1: synthetic source generation | P1-U1 |
| P1-FR-2: local lakehouse layout and Bronze ingestion | P1-U2 (consumes P1-U1 source contract) |
| P1-FR-3: Silver standardization and quality | P1-U3 |
| P1-FR-4: Gold sales and customer models | P1-U4 |
| P1-FR-5: Gold inventory and forecast models | P1-U4 |
| P1-FR-6: delivery, documentation, sample queries, and Phase 2 contract | P1-U1 through P1-U4; final integrated publication owned by P1-U4 |

### Original `requirements/phased/phase-1-lakehouse-gold-data-model.md`

| Source requirement area | Coverage |
|---|---|
| P1-FR-1A and Section 2.1: synthetic development data | P1-U1 |
| P1-FR-1: Bronze ingestion | P1-U2 |
| P1-FR-2: Silver standardization | P1-U3 |
| P1-FR-3: Gold business modeling | P1-U4 |
| P1-FR-4: sales monitoring model | P1-U4 |
| P1-FR-5: customer profile model | P1-U4 |
| P1-FR-6: product and inventory model | P1-U4 |
| Sections 7-8: phase acceptance and deliverables | P1-U1 through P1-U4; final integrated publication owned by P1-U4 |

Phase 1 acceptance criteria are covered by P1-U1/U2 for deterministic source and Bronze; P1-U3 for validated Silver; and P1-U4 for Gold, sample queries, end-to-end proof, and Phase 2 readiness.

## Ownership and Slice Constraints
- Every unit and implementation slice has the data engineer as its single accountable owner.
- Units are executed in dependency order; when a handoff fails, dependent work is held until the owning unit is corrected and its evidence passes.
- Within a unit, implementation slices are ordered milestones and do not imply parallel work or additional units.
- The same approved story IDs are preserved. All story outcomes and requirement areas have an assigned unit; cross-cutting documentation and integration evidence are assigned at the relevant unit boundary and consolidated by P1-U4.
