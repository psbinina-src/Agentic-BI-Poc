# Phase 1 Unit of Work Plan — Planning

## Purpose
Decompose the approved Phase 1 stories into development units and a single-owner sequence for one data engineer. Units are logical work groupings inside the approved modular Python application; they are not independently deployable services. Keep P1-US-1 and P1-US-2 as the two broad stories, and preserve the source Phase 1 unit IDs unless the answers below request otherwise.

## Context and Resolved Constraints
- **Owner/team**: One team with one data engineer, accountable for all units and slices. No parallel developer assignment.
- **Stories**: P1-US-1 (synthetic generation and Bronze) precedes P1-US-2 (Silver/Gold analytics models).
- **Application structure**: One local Python project; Python and SQL under `src/`, tests under `tests/`, runtime data in separate `lakehouse/source/`, `bronze/`, `silver/`, and `gold/` directories.
- **Interfaces**: Explicit CSV/Parquet file contracts and paths; stage-specific commands plus an end-to-end command.
- **Business scope**: Sales monitoring/forecasting, customer profile/repeat purchasing, and product/inventory risk.
- **Runtime**: Local DuckDB, no separately deployed services or container requirement.

## Candidate Unit Sequence
The Phase 1 source requirement proposes four units. This plan uses that structure as the baseline for discussion:

1. **P1-U1 — Synthetic generator and source contract**: Generator, configuration, deterministic seed, source entity schemas/keys, CSV files and manifest.
2. **P1-U2 — Bronze ingestion and lineage**: Repeatable CSV-to-Bronze Parquet ingestion, load metadata, source/Bronze verification, and handoff contract.
3. **P1-U3 — Silver standardization and data quality**: Typed Silver outputs, documented null/invalid/duplicate policies, quality reports, and lineage.
4. **P1-U4 — Gold models, sample queries, and Phase 2 handoff**: Sales/customer/inventory dimensional models, forecast baseline, sample queries, final Gold schemas/lineage/evidence.

**Baseline dependency**: P1-U1 -> P1-U2 -> P1-U3 -> P1-U4. Each unit is owned by the same data engineer and started after its input contract is verified. This sequence is a proposed acceptance handoff model, not parallel staffing.

## Category Assessment
- **Story grouping**: Unit count and whether to preserve source IDs is open; Question 1 asks the user to confirm or adjust the four-unit baseline.
- **Dependencies/integration**: The layer contracts are set in Application Design; the acceptance gate for each sequential unit is open; Question 2 asks how to handle a failed handoff.
- **Team alignment**: Resolved — one data engineer owns and sequences every unit; no separate ownership-boundary question is needed.
- **Technical considerations**: Resolved — one modular local Python project, file contracts, DuckDB, and no independent deployment or container needs. Technical dependency sequencing is covered by Question 2.
- **Business domain**: Resolved — the two approved stories cover source/Bronze then Silver/Gold across sales, customer, and inventory. Preserve those stories and use cases.
- **Greenfield code organization**: Resolved by approved Application Design — Python and SQL under `src/`, tests under `tests/`, and data under the dedicated root `lakehouse/`. Record this strategy in the generated `unit-of-work.md`; no repeated layout choice is needed.

## Planning Questions
Fill in every `[Answer]:` field. For `X) Other`, add the custom decision after the tag. After the answers are validated, explicitly approve this unit plan before unit artifacts are generated.

### Question 1: Unit granularity and source IDs
How should the unit structure handle the four source units P1-U1 through P1-U4?

A) Preserve all four source units in the proposed sequential order (recommended; each ends at a visible data-layer handoff)

B) Merge into two larger units: P1-U1 for generator plus Bronze, then P1-U2 for Silver plus Gold

C) Keep the four source units and add a separate unit for end-to-end integration/documentation

X) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 2: Dependency and handoff gate
What should happen when a unit's acceptance checks or data contract fail?

A) Stop before starting the dependent unit; resolve the mismatch and rerun the current unit's checks first (recommended; strict sequential handoff)

B) Continue dependent development using a clearly marked temporary contract, but block integration/acceptance until the upstream handoff passes

C) Treat all four units as one end-to-end acceptance boundary and validate only after U4

X) Other (please describe after [Answer]: tag below)

[Answer]:A

### Question 3: Unit-level acceptance evidence
What level of evidence should each unit publish at handoff?

A) A concise checklist of unit outputs, contract/quality checks, and a sample command or result proving the handoff (recommended; simple but verifiable)

B) Automated tests and a saved test/quality report for every contract, plus a manual handoff summary

C) A brief completion note and defer all acceptance evidence to the end-to-end Phase 1 gate

X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Generation Checklist — Execute After Answers and Plan Approval
- [x] Read the full approved unit plan and answers, requirements, stories, and Application Design artifacts.
- [x] Generate `aidlc-docs/inception/application-design/unit-of-work.md` with unit definitions, responsibilities, owners, acceptance outcomes, and greenfield code organization strategy.
- [x] Generate `aidlc-docs/inception/application-design/unit-of-work-dependency.md` with dependency matrix and sequential handoff rules.
- [x] Generate `aidlc-docs/inception/application-design/unit-of-work-story-map.md` mapping every approved story and requirement area to one or more units.
- [x] Validate unit boundaries, dependencies, single-owner sequence, story coverage, and acceptance gates; distinguish the clarified requirements IDs from the original source requirements IDs in the story map.
- [x] Update checkboxes and AI-DLC state immediately after each completed generation step.
- [x] Present generated unit artifacts for explicit review and approval before Construction.

## Plan Approval Gate
**Unit of work plan complete. Review the plan in `aidlc-docs/inception/plans/unit-of-work-plan.md`. Ready to proceed to generation?**
