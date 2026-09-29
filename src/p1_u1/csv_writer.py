"""Canonical CSV serialization for the P1-U1 source contract."""

from __future__ import annotations

import csv
import hashlib
from dataclasses import fields
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Iterable, TypeVar

from p1_u1.models import Customer, InventorySnapshot, OrderHeader, OrderLine, Product, SourceDataset

T = TypeVar("T")

ENTITY_FILES = {
    "customers": "customers.csv",
    "products": "products.csv",
    "orders": "orders.csv",
    "order_lines": "order_lines.csv",
    "inventory_snapshots": "inventory_snapshots.csv",
}


def _format_value(value: object) -> str:
    if isinstance(value, (date,)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return format(value, ".2f") if value.as_tuple().exponent < -2 else format(value, "f")
    return str(value)


def _write_entity(path: Path, records: Iterable[T], record_type: type[T]) -> None:
    headers = [field.name for field in fields(record_type)]
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(headers)
        for record in records:
            writer.writerow([_format_value(getattr(record, header)) for header in headers])


def write_entity_csvs(dataset: SourceDataset, output_dir: Path) -> dict[str, Path]:
    """Write all five source entities to their configured direct output paths."""
    output_dir.mkdir(parents=True, exist_ok=True)
    entities: dict[str, tuple[Iterable[object], type[object]]] = {
        "customers": (dataset.customers, Customer),
        "products": (dataset.products, Product),
        "orders": (dataset.orders, OrderHeader),
        "order_lines": (dataset.order_lines, OrderLine),
        "inventory_snapshots": (dataset.inventory_snapshots, InventorySnapshot),
    }
    outputs: dict[str, Path] = {}
    for entity_name, (records, record_type) in entities.items():
        path = output_dir / ENTITY_FILES[entity_name]
        _write_entity(path, records, record_type)
        outputs[entity_name] = path
    return outputs


def file_sha256(path: Path) -> str:
    """Return a stable SHA-256 checksum for a source file."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
