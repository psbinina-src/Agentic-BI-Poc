import json
from hashlib import sha256
from pathlib import Path

from p1_u2.cli import main


def _make_csv(path: Path, contents: str) -> None:
    path.write_text(contents, encoding="utf-8")


def _checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def test_cli_returns_success_for_good_source(tmp_path: Path) -> None:
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    bronze_dir = tmp_path / "bronze"
    file_defs = {
        "customers": "customer_id,customer_name\nC1,Alice\nC2,Bob\n",
        "products": "product_id,product_name\nP1,Widget\nP2,Gadget\n",
        "orders": "order_id,customer_id\nO1,C1\nO2,C2\n",
        "order_lines": "order_line_id,order_id,product_id\nL1,O1,P1\nL2,O1,P2\n",
        "inventory_snapshots": "snapshot_date,product_id\n2024-01-01,P1\n2024-01-01,P2\n",
    }
    for name, contents in file_defs.items():
        _make_csv(source_dir / f"{name}.csv", contents)

    manifest = {
        "validation": {"passed": True},
        "checksums": {name: _checksum(source_dir / f"{name}.csv") for name in file_defs},
    }
    (source_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    result = main(["--source-dir", str(source_dir), "--bronze-dir", str(bronze_dir)])
    assert result == 0


def test_cli_returns_nonzero_for_invalid_source(tmp_path: Path) -> None:
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    result = main(["--source-dir", str(source_dir), "--bronze-dir", str(tmp_path / "bronze")])
    assert result == 1
