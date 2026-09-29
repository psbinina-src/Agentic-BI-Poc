from __future__ import annotations

import json
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

import duckdb

from p1_u2.config import BronzeConfig

ENTITY_FILES = {
    "customers": "customers.csv",
    "products": "products.csv",
    "orders": "orders.csv",
    "order_lines": "order_lines.csv",
    "inventory_snapshots": "inventory_snapshots.csv",
}


def _hash_file(path: Path) -> str:
    h = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_manifest(source_dir: Path) -> dict:
    manifest_path = source_dir / "manifest.json"
    if not manifest_path.exists():
        raise ValueError(f"Missing source manifest: {manifest_path}")
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def _validate_manifest(manifest: dict, source_dir: Path) -> None:
    if not manifest.get("validation", {}).get("passed"):
        raise ValueError("Source manifest validation is false")
    checksums = manifest.get("checksums", {})
    if not checksums:
        raise ValueError("Source manifest is missing checksum metadata")
    for entity_name, filename in ENTITY_FILES.items():
        file_path = source_dir / filename
        if not file_path.exists():
            raise ValueError(f"Missing required source file: {filename}")
        expected_hash = checksums.get(entity_name)
        if expected_hash is None:
            raise ValueError(f"Missing checksum for {entity_name}")
        actual_hash = _hash_file(file_path)
        if actual_hash != expected_hash:
            raise ValueError(f"checksum mismatch for {entity_name}: expected {expected_hash}, got {actual_hash}")


def _read_csv_with_lineage(path: Path, filename: str, run_id: str) -> duckdb.DuckDBPyRelation:
    csv_path = str(path).replace("\\", "/")
    sql = (
        "SELECT *, "
        f"'{filename}' AS source_file, "
        "row_number() OVER () AS source_row_number, "
        f"'{run_id}' AS source_run_id, "
        "CURRENT_TIMESTAMP AS ingested_at "
        f"FROM read_csv_auto('{csv_path}', header = true)"
    )
    return duckdb.sql(sql)


def ingest_source_to_bronze(config: BronzeConfig) -> dict[str, duckdb.DuckDBPyRelation]:
    source_dir = Path(config.source_dir)
    bronze_dir = Path(config.bronze_dir)
    bronze_dir.mkdir(parents=True, exist_ok=True)
    manifest = _load_manifest(source_dir)
    _validate_manifest(manifest, source_dir)

    run_id = config.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outputs: dict[str, duckdb.DuckDBPyRelation] = {}
    for entity_name, filename in ENTITY_FILES.items():
        source_path = source_dir / filename
        with_ledger = _read_csv_with_lineage(source_path, filename, run_id)
        target_path = bronze_dir / f"{entity_name}.parquet"
        with_ledger.write_parquet(str(target_path))
        outputs[entity_name] = duckdb.read_parquet(str(target_path))
    return outputs
