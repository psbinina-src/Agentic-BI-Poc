"""Typed source entities and generator result models for P1-U1."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class Customer:
    customer_id: str
    customer_name: str
    customer_segment: str
    region: str
    acquisition_channel: str
    acquisition_date: date
    customer_status: str


@dataclass(frozen=True, slots=True)
class Product:
    product_id: str
    product_name: str
    category: str
    subcategory: str
    list_price: Decimal
    reorder_point: int
    product_status: str


@dataclass(frozen=True, slots=True)
class OrderHeader:
    order_id: str
    customer_id: str
    order_date: date
    order_status: str
    payment_method: str
    channel: str


@dataclass(frozen=True, slots=True)
class OrderLine:
    order_line_id: str
    order_id: str
    product_id: str
    quantity: int
    unit_price: Decimal
    discount_rate: Decimal


@dataclass(frozen=True, slots=True)
class InventorySnapshot:
    snapshot_date: date
    product_id: str
    inventory_on_hand: int
    reorder_point: int


@dataclass(slots=True)
class SourceDataset:
    customers: list[Customer] = field(default_factory=list)
    products: list[Product] = field(default_factory=list)
    orders: list[OrderHeader] = field(default_factory=list)
    order_lines: list[OrderLine] = field(default_factory=list)
    inventory_snapshots: list[InventorySnapshot] = field(default_factory=list)

    def entity_counts(self) -> dict[str, int]:
        return {
            "customers": len(self.customers),
            "products": len(self.products),
            "orders": len(self.orders),
            "order_lines": len(self.order_lines),
            "inventory_snapshots": len(self.inventory_snapshots),
        }


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    message: str
    entity: str | None = None

    def to_dict(self) -> dict[str, str]:
        result = {"code": self.code, "message": self.message}
        if self.entity is not None:
            result["entity"] = self.entity
        return result


@dataclass(frozen=True, slots=True)
class ValidationReport:
    issues: tuple[ValidationIssue, ...] = ()
    scenarios: dict[str, bool] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return not self.issues and all(self.scenarios.values())

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "issues": [issue.to_dict() for issue in self.issues],
            "scenarios": dict(sorted(self.scenarios.items())),
        }


@dataclass(frozen=True, slots=True)
class GenerationManifest:
    schema_version: str
    seed: int
    start_date: date
    end_date: date
    requested_volumes: dict[str, int]
    actual_counts: dict[str, int]
    output_files: dict[str, str]
    checksums: dict[str, str]
    validation: ValidationReport
    generated_at: datetime
    manifest_path: Path

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "seed": self.seed,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "requested_volumes": dict(sorted(self.requested_volumes.items())),
            "actual_counts": dict(sorted(self.actual_counts.items())),
            "output_files": dict(sorted(self.output_files.items())),
            "checksums": dict(sorted(self.checksums.items())),
            "validation": self.validation.to_dict(),
            "generated_at": self.generated_at.isoformat(),
        }


@dataclass(frozen=True, slots=True)
class GenerationResult:
    dataset: SourceDataset
    validation: ValidationReport
    elapsed_seconds: float
    manifest: GenerationManifest | None = None
