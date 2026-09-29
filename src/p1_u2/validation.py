from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

ENTITY_FILES = {
    "customers": "customers.csv",
    "products": "products.csv",
    "orders": "orders.csv",
    "order_lines": "order_lines.csv",
    "inventory_snapshots": "inventory_snapshots.csv",
}


def read_manifest(source_dir: Path) -> dict:
    manifest_path = source_dir / "manifest.json"
    if not manifest_path.exists():
        raise ValueError(f"Missing source manifest: {manifest_path}")
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid source manifest JSON: {manifest_path}") from exc


def hash_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_source_contract(source_dir: Path) -> dict:
    manifest = read_manifest(source_dir)
    if not manifest.get("validation", {}).get("passed"):
        raise ValueError("Source manifest validation is false")

    checksums = manifest.get("checksums", {})
    if not checksums:
        raise ValueError("Source manifest is missing checksum metadata")

    for entity_name, file_name in ENTITY_FILES.items():
        file_path = source_dir / file_name
        if not file_path.exists():
            raise ValueError(f"Missing required source file: {file_name}")
        expected = checksums.get(entity_name)
        if expected is None:
            raise ValueError(f"Missing checksum for {entity_name}")
        actual = hash_file(file_path)
        if actual != expected:
            raise ValueError(f"checksum mismatch for {entity_name}: expected {expected}, got {actual}")

    return manifest
