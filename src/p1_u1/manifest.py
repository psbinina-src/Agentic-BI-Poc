"""Success-manifest creation for completed P1-U1 source runs."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from p1_u1.config import GeneratorConfig
from p1_u1.csv_writer import file_sha256
from p1_u1.models import GenerationManifest, SourceDataset, ValidationReport

MANIFEST_FILENAME = "manifest.json"


def publish_success_manifest(
    config: GeneratorConfig,
    dataset: SourceDataset,
    validation: ValidationReport,
    output_files: dict[str, Path],
) -> GenerationManifest:
    """Publish a success marker after all source CSVs have been written."""
    manifest_path = config.output_dir / MANIFEST_FILENAME
    manifest = GenerationManifest(
        schema_version=config.schema_version,
        seed=config.seed,
        start_date=config.start_date,
        end_date=config.end_date,
        requested_volumes=config.requested_volumes(),
        actual_counts=dataset.entity_counts(),
        output_files={name: str(path.resolve()) for name, path in output_files.items()},
        checksums={name: file_sha256(path) for name, path in output_files.items()},
        validation=validation,
        generated_at=datetime.now(timezone.utc),
        manifest_path=manifest_path,
    )
    try:
        manifest_path.write_text(
            json.dumps(manifest.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    except OSError:
        manifest_path.unlink(missing_ok=True)
        raise
    return manifest
