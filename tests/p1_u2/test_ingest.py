from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from p1_u2.config import BronzeConfig
from p1_u2.ingest import ingest_source_to_bronze


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _make_manifest(source_dir: Path) -> dict:
    payload = {
        "schema_version": "1.0.0",
        "validation": {"passed": True},
        "requested_volumes": {"customers": 2, "products": 2, "orders": 2, "order_lines": 3, "inventory_snapshots": 6},
        "actual_counts": {"customers": 2, "products": 2, "orders": 2, "order_lines": 3, "inventory_snapshots": 6},
        "output_files": {
            "customers": str((source_dir / "customers.csv").resolve()),
            "products": str((source_dir / "products.csv").resolve()),
            "orders": str((source_dir / "orders.csv").resolve()),
            "order_lines": str((source_dir / "order_lines.csv").resolve()),
            "inventory_snapshots": str((source_dir / "inventory_snapshots.csv").resolve()),
        },
    }
    for name in ["customers", "products", "orders", "order_lines", "inventory_snapshots"]:
        path = source_dir / f"{name}.csv"
        payload["checksums"] = payload.get("checksums", {})
        payload["checksums"][name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return payload


def test_ingest_successfully_reads_source_and_writes_bronze(tmp_path: Path) -> None:
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    _write_csv(
        source_dir / "customers.csv",
        ["customer_id", "customer_name", "customer_segment"],
        [{"customer_id": "C1", "customer_name": "Alice", "customer_segment": "Plus"}, {"customer_id": "C2", "customer_name": "Bob", "customer_segment": "Standard"}],
    )
    _write_csv(
        source_dir / "products.csv",
        ["product_id", "product_name", "category"],
        [{"product_id": "P1", "product_name": "Widget", "category": "Electronics"}, {"product_id": "P2", "product_name": "Gadget", "category": "Home"}],
    )
    _write_csv(
        source_dir / "orders.csv",
        ["order_id", "customer_id", "order_date", "order_status"],
        [{"order_id": "O1", "customer_id": "C1", "order_date": "2024-01-01", "order_status": "Completed"}, {"order_id": "O2", "customer_id": "C2", "order_date": "2024-01-02", "order_status": "Cancelled"}],
    )
    _write_csv(
        source_dir / "order_lines.csv",
        ["order_line_id", "order_id", "product_id", "quantity"],
        [{"order_line_id": "L1", "order_id": "O1", "product_id": "P1", "quantity": "2"}, {"order_line_id": "L2", "order_id": "O1", "product_id": "P2", "quantity": "1"}, {"order_line_id": "L3", "order_id": "O2", "product_id": "P1", "quantity": "3"}],
    )
    _write_csv(
        source_dir / "inventory_snapshots.csv",
        ["snapshot_date", "product_id", "inventory_on_hand", "reorder_point"],
        [
            {"snapshot_date": "2024-01-01", "product_id": "P1", "inventory_on_hand": "10", "reorder_point": "5"},
            {"snapshot_date": "2024-01-01", "product_id": "P2", "inventory_on_hand": "8", "reorder_point": "4"},
            {"snapshot_date": "2024-01-02", "product_id": "P1", "inventory_on_hand": "9", "reorder_point": "5"},
            {"snapshot_date": "2024-01-02", "product_id": "P2", "inventory_on_hand": "7", "reorder_point": "4"},
            {"snapshot_date": "2024-01-03", "product_id": "P1", "inventory_on_hand": "11", "reorder_point": "5"},
            {"snapshot_date": "2024-01-03", "product_id": "P2", "inventory_on_hand": "9", "reorder_point": "4"},
        ],
    )
    manifest = _make_manifest(source_dir)
    (source_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    bronze_dir = tmp_path / "bronze"
    config = BronzeConfig(source_dir=source_dir, bronze_dir=bronze_dir)
    result = ingest_source_to_bronze(config)

    assert result["customers"].shape[0] == 2
    assert "source_file" in result["customers"].columns
    unique_runs = len(result["customers"].select("source_run_id").distinct().fetchall())
    assert unique_runs == 1
    assert (bronze_dir / "customers.parquet").exists()


def test_ingest_fails_on_checksum_mismatch(tmp_path: Path) -> None:
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    for name, fieldnames, rows in [
        ("customers", ["customer_id", "customer_name"], [{"customer_id": "C1", "customer_name": "Alice"}]),
        ("products", ["product_id", "product_name"], [{"product_id": "P1", "product_name": "Widget"}]),
        ("orders", ["order_id", "customer_id"], [{"order_id": "O1", "customer_id": "C1"}]),
        ("order_lines", ["order_line_id", "order_id", "product_id"], [{"order_line_id": "L1", "order_id": "O1", "product_id": "P1"}]),
        ("inventory_snapshots", ["snapshot_date", "product_id"], [{"snapshot_date": "2024-01-01", "product_id": "P1"}]),
    ]:
        _write_csv(source_dir / f"{name}.csv", fieldnames, rows)
    manifest = _make_manifest(source_dir)
    manifest["checksums"]["customers"] = "deadbeef"
    (source_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    config = BronzeConfig(source_dir=source_dir, bronze_dir=tmp_path / "bronze")
    with pytest.raises(ValueError, match="checksum"):
        ingest_source_to_bronze(config)
