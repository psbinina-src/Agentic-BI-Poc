from pathlib import Path

import pytest

from p1_u2.validation import validate_source_contract


def test_validate_source_contract_rejects_missing_manifest(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Missing source manifest"):
        validate_source_contract(tmp_path)


def test_validate_source_contract_rejects_missing_file(tmp_path: Path) -> None:
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    manifest = {
        "validation": {"passed": True},
        "checksums": {"customers": "abc", "products": "def", "orders": "ghi", "order_lines": "jkl", "inventory_snapshots": "mno"},
    }
    (source_dir / "manifest.json").write_text(__import__("json").dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="Missing required source file"):
        validate_source_contract(source_dir)
