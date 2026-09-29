# Phase 1 Personas

## Data Engineer
- **Archetype**: The single accountable implementer for Phase 1 data generation, ingestion, transformations, tests, documentation, and integration.
- **Needs**: Deterministic synthetic inputs; clear schemas, keys, and layer contracts; repeatable local commands; inspectable data-quality results; a sequenced plan with verifiable acceptance and no conflicting ownership.
- **Constraint**: One data engineer performs the work; dependent slices are sequenced rather than assigned to parallel owners.
- **Mapped story**: P1-US-1. Also acts as the implementer of P1-US-2.

## Analytics Consumer
- **Archetype**: A business or analytics user consuming curated Phase 1 outputs to inspect sales, customer behavior, and inventory health.
- **Needs**: Clean and understandable business-ready data with stable measures and dimensions, useful grains, and example queries for common questions.
- **Mapped story**: P1-US-2.

## Persona-to-Story Map
| Persona | Story | Value |
|---|---|---|
| Data Engineer | P1-US-1 | Creates repeatable, traceable source and Bronze inputs. |
| Data Engineer | P1-US-2 | Delivers quality-controlled, documented Silver/Gold outputs and the downstream handoff. |
| Analytics Consumer | P1-US-2 | Uses Gold outputs to analyze sales, customers, and inventory. |
