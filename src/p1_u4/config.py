from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GoldConfig:
    silver_dir: Path = Path("lakehouse/silver")
    gold_dir: Path = Path("lakehouse/gold")
