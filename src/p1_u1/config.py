"""Configuration loading and validation for the P1-U1 generator."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


DEFAULT_CONFIG_PATH = Path("config/p1-u1-defaults.toml")
DEFAULT_OUTPUT_DIR = Path("lakehouse/source")


class ConfigurationError(ValueError):
    """Raised when the generator configuration is incomplete or invalid."""


@dataclass(frozen=True, slots=True)
class GeneratorConfig:
    seed: int
    start_date: date
    end_date: date
    customer_count: int
    product_count: int
    order_line_count: int
    output_dir: Path
    schema_version: str = "1.0.0"

    @property
    def inventory_snapshot_count(self) -> int:
        return self.product_count * ((self.end_date - self.start_date).days + 1)

    def requested_volumes(self) -> dict[str, int]:
        return {
            "customers": self.customer_count,
            "products": self.product_count,
            "order_lines": self.order_line_count,
            "inventory_snapshots": self.inventory_snapshot_count,
        }


def _parse_date(value: Any, name: str) -> date:
    if not isinstance(value, str):
        raise ConfigurationError(f"{name} must be an ISO date string (YYYY-MM-DD)")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be a valid ISO date (YYYY-MM-DD)") from exc


def _positive_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ConfigurationError(f"{name} must be a positive integer")
    return value


def load_config(
    config_path: Path | None = None,
    *,
    seed: int | None = None,
    start_date: str | date | None = None,
    end_date: str | date | None = None,
    customer_count: int | None = None,
    product_count: int | None = None,
    order_line_count: int | None = None,
    output_dir: Path | None = None,
) -> GeneratorConfig:
    """Load TOML defaults, apply explicit overrides, and validate effective values."""
    path = config_path or DEFAULT_CONFIG_PATH
    if path.exists():
        try:
            with path.open("rb") as stream:
                loaded = tomllib.load(stream)
        except (OSError, tomllib.TOMLDecodeError) as exc:
            raise ConfigurationError(f"could not read config file {path}: {exc}") from exc
        raw = loaded.get("generator", {})
        if not isinstance(raw, dict):
            raise ConfigurationError("[generator] configuration section must be a table")
    elif config_path is not None:
        raise ConfigurationError(f"config file does not exist: {path}")
    else:
        raw = {
            "seed": 42,
            "start_date": "2023-01-01",
            "end_date": "2025-12-31",
            "customer_count": 10000,
            "product_count": 1000,
            "order_line_count": 100000,
            "output_dir": str(DEFAULT_OUTPUT_DIR),
        }

    effective_seed = seed if seed is not None else raw.get("seed", 42)
    if isinstance(effective_seed, bool) or not isinstance(effective_seed, int):
        raise ConfigurationError("seed must be an integer")

    raw_start = start_date if start_date is not None else raw.get("start_date", "2023-01-01")
    raw_end = end_date if end_date is not None else raw.get("end_date", "2025-12-31")
    parsed_start = raw_start if isinstance(raw_start, date) else _parse_date(raw_start, "start_date")
    parsed_end = raw_end if isinstance(raw_end, date) else _parse_date(raw_end, "end_date")
    if parsed_end < parsed_start:
        raise ConfigurationError("end_date must be on or after start_date")

    counts = {
        "customer_count": customer_count if customer_count is not None else raw.get("customer_count", 10000),
        "product_count": product_count if product_count is not None else raw.get("product_count", 1000),
        "order_line_count": order_line_count if order_line_count is not None else raw.get("order_line_count", 100000),
    }
    validated_counts = {name: _positive_int(value, name) for name, value in counts.items()}
    raw_output = output_dir if output_dir is not None else raw.get("output_dir", str(DEFAULT_OUTPUT_DIR))
    if not isinstance(raw_output, (str, Path)) or not str(raw_output).strip():
        raise ConfigurationError("output_dir must be a non-empty path")
    effective_output = Path(raw_output)

    return GeneratorConfig(
        seed=effective_seed,
        start_date=parsed_start,
        end_date=parsed_end,
        customer_count=validated_counts["customer_count"],
        product_count=validated_counts["product_count"],
        order_line_count=validated_counts["order_line_count"],
        output_dir=effective_output,
    )
