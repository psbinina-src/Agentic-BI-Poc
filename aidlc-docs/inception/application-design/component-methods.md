# Phase 1 Component Method Interfaces

These are high-level Python interface sketches to guide module boundaries. They are not committed implementation code; concrete models, schemas, flags, exceptions, and detailed business logic are defined during Functional Design and Code Generation.

## Shared Types

```python
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

@dataclass(frozen=True)
class PipelineConfig:
    seed: int
    start_date: str
    end_date: str
    customer_count: int
    product_count: int
    order_line_count: int
    source_dir: Path
    bronze_dir: Path
    silver_dir: Path
    gold_dir: Path

@dataclass(frozen=True)
class StageResult:
    stage: str
    status: str
    outputs: Mapping[str, Path]
    counts: Mapping[str, int]
    messages: Sequence[str]

@dataclass(frozen=True)
class QualityReport:
    passed: bool
    checks: Sequence[Mapping[str, object]]
    summary: str
```

## Configuration and Paths
- `load_config(config_path: Path | None) -> PipelineConfig`: load defaults and user overrides, then validate required configuration fields.
- `resolve_layer_paths(config: PipelineConfig) -> Mapping[str, Path]`: return configured source and layer paths.

## Synthetic Source Generator
- `generate_source_data(config: PipelineConfig) -> StageResult`: generate the configured synthetic entities, write CSV inputs and a run manifest, and report outputs/counts.
- `write_source_manifest(config: PipelineConfig, outputs: Mapping[str, Path], counts: Mapping[str, int]) -> Path`: persist provenance and generation settings without sensitive values.

## Bronze Ingestion
- `ingest_bronze(config: PipelineConfig, manifest_path: Path | None = None) -> StageResult`: load the configured CSV inputs and publish Bronze Parquet datasets with ingestion metadata.

## Silver and Gold Transformation
- `build_silver(config: PipelineConfig) -> StageResult`: run Silver SQL over Bronze inputs and publish standardized Parquet datasets.
- `build_gold(config: PipelineConfig) -> StageResult`: run Gold SQL over Silver inputs and publish business-ready Parquet datasets.
- `run_transformations(config: PipelineConfig) -> StageResult`: execute Silver then Gold, stopping when a required prior stage fails.

## Data Quality
- `validate_source(config: PipelineConfig) -> QualityReport`: validate source file presence and source-contract checks.
- `validate_layer(layer: str, config: PipelineConfig) -> QualityReport`: run the configured checks for the named layer and report results.
- `write_quality_report(report: QualityReport, output_path: Path) -> Path`: persist inspectable quality evidence.

## Gold Query and Demo Helpers
- `run_sample_query(query_name: str, config: PipelineConfig, parameters: Mapping[str, object] | None = None) -> Sequence[Mapping[str, object]]`: execute an approved sample Gold query and return tabular rows.
- `run_phase1_demos(config: PipelineConfig) -> Mapping[str, Sequence[Mapping[str, object]]]`: run the sales trend, repeat-purchase, and inventory-risk examples.

## Pipeline Orchestration
- `run_stage(stage: str, config: PipelineConfig) -> StageResult`: dispatch one named stage.
- `run_pipeline(config: PipelineConfig, *, include_generation: bool = True) -> Sequence[StageResult]`: execute generation, Bronze ingestion, transformations, validations, and optional demos in dependency order.
- `main(argv: Sequence[str] | None = None) -> int`: parse the CLI command/configuration, invoke one stage or the end-to-end run, and return a process status.

## Interface Notes
- Commands pass configuration and local paths, not dataset contents, across stage boundaries.
- CSV and Parquet are the published data contracts. DuckDB connections are opened within the stage that executes SQL and are not long-lived cross-stage services.
- `StageResult` and `QualityReport` names describe conceptual output contracts; precise fields and serialization formats will be finalized in detailed design.
- No network/API interfaces or external runtime dependencies are defined for Phase 1.
