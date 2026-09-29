import csv
import json
from datetime import date
from pathlib import Path

import pytest

from p1_u1.config import GeneratorConfig
from p1_u1 import cli
from p1_u1.manifest import MANIFEST_FILENAME


def test_outputs_are_canonical_and_manifest_is_published_last(tmp_path: Path) -> None:
    config = GeneratorConfig(42, date(2024, 1, 1), date(2024, 2, 29), 20, 10, 100, tmp_path)
    first = cli.run_generation(config)
    manifest_path = tmp_path / MANIFEST_FILENAME
    first_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    first_checksums = first_manifest["checksums"]

    with (tmp_path / "customers.csv").open(encoding="utf-8", newline="") as stream:
        reader = csv.reader(stream)
        assert next(reader) == [
            "customer_id", "customer_name", "customer_segment", "region",
            "acquisition_channel", "acquisition_date", "customer_status",
        ]

    second = cli.run_generation(config)
    second_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert first_checksums == second_manifest["checksums"]
    assert first.dataset == second.dataset
    assert second.elapsed_seconds >= 0


def test_failed_csv_write_removes_success_manifest_and_returns_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config = GeneratorConfig(42, date(2024, 1, 1), date(2024, 2, 29), 20, 10, 100, tmp_path)
    cli.run_generation(config)
    manifest_path = tmp_path / MANIFEST_FILENAME
    assert manifest_path.exists()

    def fail_write(*args: object, **kwargs: object) -> dict[str, Path]:
        raise OSError("simulated write failure")

    monkeypatch.setattr(cli, "write_entity_csvs", fail_write)
    with pytest.raises(OSError, match="simulated write failure"):
        cli.run_generation(config)
    assert not manifest_path.exists()
