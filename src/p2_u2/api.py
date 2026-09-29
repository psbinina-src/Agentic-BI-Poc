from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from p2_u2.gold_access import DATASETS, GoldDataAccess


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_GOLD_DIR = WORKSPACE_ROOT / "lakehouse" / "gold"


class FilterSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field: str
    operator: Literal["eq", "ne", "gt", "gte", "lt", "lte", "in"]
    value: Any


class AggregationSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field: str
    function: Literal["sum", "avg", "min", "max", "count", "count_distinct"]


class SortSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field: str
    direction: Literal["asc", "desc"] = "asc"


class QueryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dataset: str
    fields: list[str] = Field(default_factory=list, max_length=20)
    joins: list[str] = Field(default_factory=list, max_length=3)
    filters: list[FilterSpec] = Field(default_factory=list, max_length=20)
    group_by: list[str] = Field(default_factory=list, max_length=10)
    aggregations: list[AggregationSpec] = Field(default_factory=list, max_length=10)
    order_by: list[SortSpec] = Field(default_factory=list, max_length=10)
    limit: int = Field(default=100, ge=1, le=500)


def create_app(gold_dir: Path | None = None) -> FastAPI:
    configured_dir = gold_dir or Path(os.environ.get("AGENTIC_BI_GOLD_DIR", DEFAULT_GOLD_DIR))
    access = GoldDataAccess(configured_dir)
    app = FastAPI(
        title="Agentic BI Gold Data API",
        description="Read-only local catalogue and query access to the Phase 1 Gold Parquet datasets.",
        version="0.1.0",
    )
    app.state.gold_access = access

    @app.get("/health", tags=["system"])
    def health() -> dict[str, Any]:
        available = sum(item["available"] for item in access.catalog())
        return {"status": "ok" if available == len(DATASETS) else "degraded", "gold_datasets_available": available}

    @app.get("/catalog", tags=["catalog"])
    def catalog() -> dict[str, Any]:
        return {"datasets": access.catalog(), "relationships": access.relationships()}

    @app.get("/catalog/{dataset}", tags=["catalog"])
    def dataset_details(dataset: str) -> dict[str, Any]:
        try:
            return access.dataset_details(dataset)
        except KeyError:
            raise HTTPException(status_code=404, detail="Unknown Gold dataset.") from None
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Gold dataset is not available.") from None

    @app.post("/query", tags=["data"])
    def query(request: QueryRequest) -> dict[str, Any]:
        try:
            return access.query(request)
        except KeyError:
            raise HTTPException(status_code=404, detail="Unknown Gold dataset.") from None
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Gold dataset is not available.") from None
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from None

    return app


app = create_app()
