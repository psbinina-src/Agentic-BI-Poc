from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SilverConfig:
    bronze_dir: Path = Path("lakehouse/bronze")
    silver_dir: Path = Path("lakehouse/silver")
    run_id: str | None = None
