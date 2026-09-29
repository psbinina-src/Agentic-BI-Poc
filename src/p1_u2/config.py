from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BronzeConfig:
    source_dir: Path = Path("lakehouse/source")
    bronze_dir: Path = Path("lakehouse/bronze")
    run_id: str | None = None
