from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import duckdb


@dataclass(frozen=True)
class Dataset:
    name: str
    description: str
    grain: str
    key_fields: tuple[str, ...]


DATASETS = {
    "sales_gold": Dataset(
        "sales_gold",
        "Completed order-line sales, with customer, product, channel, and revenue fields.",
        "One row per completed order line.",
        ("order_line_id",),
    ),
    "customers_gold": Dataset(
        "customers_gold",
        "Customer profile and acquisition attributes.",
        "One row per customer.",
        ("customer_id",),
    ),
    "products_gold": Dataset(
        "products_gold",
        "Product catalogue and category attributes.",
        "One row per product.",
        ("product_id",),
    ),
    "inventory_gold": Dataset(
        "inventory_gold",
        "Daily inventory, velocity, and stock-coverage snapshot by product.",
        "One row per product per snapshot date.",
        ("snapshot_date", "product_id"),
    ),
}

RELATIONSHIPS = (
    {
        "from_dataset": "sales_gold",
        "from_field": "customer_id",
        "to_dataset": "customers_gold",
        "to_field": "customer_id",
        "cardinality": "many_to_one",
        "join_type": "left",
    },
    {
        "from_dataset": "sales_gold",
        "from_field": "product_id",
        "to_dataset": "products_gold",
        "to_field": "product_id",
        "cardinality": "many_to_one",
        "join_type": "left",
    },
    {
        "from_dataset": "inventory_gold",
        "from_field": "product_id",
        "to_dataset": "products_gold",
        "to_field": "product_id",
        "cardinality": "many_to_one",
        "join_type": "left",
    },
)

FIELD_DESCRIPTIONS = {
    "order_line_id": "Unique identifier for the order line.",
    "order_id": "Identifier shared by lines belonging to the same order.",
    "product_id": "Gold product key.",
    "customer_id": "Gold customer key.",
    "order_date": "Date the completed order was placed.",
    "channel": "Sales channel for the completed order.",
    "quantity": "Units sold on the order line.",
    "unit_price": "Unit selling price before discount.",
    "discount_rate": "Discount rate applied to the order line.",
    "gross_sales_amount": "Quantity multiplied by unit price before discount.",
    "discount_amount": "Discount amount for the order line.",
    "net_sales_amount": "Gross sales less discount for the order line.",
    "customer_segment": "Gold customer segment.",
    "region": "Customer region.",
    "acquisition_channel": "Channel through which the customer was acquired.",
    "acquisition_date": "Date the customer was acquired.",
    "customer_status": "Current customer status in the Gold model.",
    "product_name": "Readable product name.",
    "category": "Product category.",
    "subcategory": "Product subcategory.",
    "list_price": "Current listed product price.",
    "product_status": "Current product status in the Gold model.",
    "snapshot_date": "Date of the inventory snapshot.",
    "inventory_on_hand": "Units on hand at the snapshot date.",
    "reorder_point": "Inventory threshold used for the low-stock flag.",
    "sales_velocity_units_per_day": "Completed units sold per day over the preceding 30 full calendar days.",
    "stock_coverage_days": "On-hand units divided by daily sales velocity; zero when velocity is zero.",
    "stock_coverage_status": "Coverage calculation status: calculated or no_demand.",
    "low_stock_flag": "True when on-hand inventory is at or below the reorder point.",
}


class GoldDataAccess:
    def __init__(self, gold_dir: Path) -> None:
        self.gold_dir = gold_dir.expanduser().resolve()

    def catalog(self) -> list[dict[str, Any]]:
        return [
            {
                "name": dataset.name,
                "description": dataset.description,
                "grain": dataset.grain,
                "key_fields": list(dataset.key_fields),
                "available": self._path(dataset.name).is_file(),
            }
            for dataset in DATASETS.values()
        ]

    def relationships(self, dataset_name: str | None = None) -> list[dict[str, Any]]:
        return [
            dict(relationship)
            for relationship in RELATIONSHIPS
            if dataset_name is None
            or relationship["from_dataset"] == dataset_name
            or relationship["to_dataset"] == dataset_name
        ]

    def dataset_details(self, name: str) -> dict[str, Any]:
        dataset = self._get_dataset(name)
        path = self._path(name)
        if not path.is_file():
            raise FileNotFoundError(name)

        with duckdb.connect() as connection:
            schema = connection.execute(
                "DESCRIBE SELECT * FROM read_parquet(?)", [str(path)]
            ).fetchall()

        return {
            "name": dataset.name,
            "description": dataset.description,
            "grain": dataset.grain,
            "key_fields": list(dataset.key_fields),
            "relationships": self.relationships(name),
            "fields": [
                {
                    "name": field_name,
                    "type": field_type,
                    "description": FIELD_DESCRIPTIONS.get(field_name, ""),
                }
                for field_name, field_type, *_ in schema
            ],
        }

    def query(self, request: Any) -> dict[str, Any]:
        dataset = self._get_dataset(request.dataset)
        path = self._path(dataset.name)
        if not path.is_file():
            raise FileNotFoundError(dataset.name)

        joined_datasets = list(request.joins)
        if len(set(joined_datasets)) != len(joined_datasets) or dataset.name in joined_datasets:
            raise ValueError("Join datasets must be unique and cannot repeat the base dataset.")
        schemas: dict[str, dict[str, str]] = {dataset.name: self._field_types(dataset.name)}
        from_parts = [f"read_parquet(?) AS {_quote(dataset.name)}"]
        parameters: list[Any] = [str(path)]
        for joined_name in joined_datasets:
            self._get_dataset(joined_name)
            relationship = next(
                (
                    item
                    for item in RELATIONSHIPS
                    if item["from_dataset"] == dataset.name and item["to_dataset"] == joined_name
                ),
                None,
            )
            if relationship is None:
                raise ValueError(f"No approved Gold relationship joins {dataset.name} to {joined_name}.")
            joined_path = self._path(joined_name)
            if not joined_path.is_file():
                raise FileNotFoundError(joined_name)
            schemas[joined_name] = self._field_types(joined_name)
            from_parts.append(
                f"LEFT JOIN read_parquet(?) AS {_quote(joined_name)} "
                f"ON {_quote(dataset.name)}.{_quote(relationship['from_field'])} "
                f"= {_quote(joined_name)}.{_quote(relationship['to_field'])}"
            )
            parameters.append(str(joined_path))

        referenced_fields = list(request.fields) + list(request.group_by)
        referenced_fields += [item.field for item in request.filters]
        referenced_fields += [item.field for item in request.aggregations]
        resolved_fields = {name: _resolve_field(name, schemas) for name in set(referenced_fields)}

        if request.aggregations:
            if request.fields:
                raise ValueError("Use either fields or aggregations, not both.")
            if len(set(request.group_by)) != len(request.group_by):
                raise ValueError("group_by fields must be unique.")
            select_parts = [
                f"{_qualified(resolved_fields[field])} AS {_quote(field)}"
                for field in request.group_by
            ]
            output_fields = set(request.group_by)
            for aggregation in request.aggregations:
                source_dataset, source_field = resolved_fields[aggregation.field]
                field_type = schemas[source_dataset][source_field]
                if aggregation.function in {"sum", "avg"} and not _is_numeric(field_type):
                    raise ValueError(f"{aggregation.function} requires a numeric field.")
                alias = f"{aggregation.function}_{aggregation.field.replace('.', '_')}"
                field_sql = _qualified(resolved_fields[aggregation.field])
                if aggregation.function == "count_distinct":
                    expression = f"COUNT(DISTINCT {field_sql})"
                else:
                    expression = f"{aggregation.function.upper()}({field_sql})"
                select_parts.append(f"{expression} AS {_quote(alias)}")
                output_fields.add(alias)
        else:
            if request.group_by:
                raise ValueError("group_by requires at least one aggregation.")
            if not request.fields:
                raise ValueError("Select fields or provide aggregations.")
            if len(set(request.fields)) != len(request.fields):
                raise ValueError("fields must be unique.")
            select_parts = [
                f"{_qualified(resolved_fields[field])} AS {_quote(field)}"
                for field in request.fields
            ]
            output_fields = set(request.fields)

        if not select_parts:
            raise ValueError("The query must select at least one field.")
        if any(sort.field not in output_fields for sort in request.order_by):
            raise ValueError("order_by fields must be selected in the query result.")

        conditions: list[str] = []
        sql_operators = {"eq": "=", "ne": "<>", "gt": ">", "gte": ">=", "lt": "<", "lte": "<="}
        for condition in request.filters:
            field_sql = _qualified(resolved_fields[condition.field])
            if condition.operator == "in":
                if not isinstance(condition.value, list) or not condition.value:
                    raise ValueError("The in operator requires a non-empty list of values.")
                if len(condition.value) > 100:
                    raise ValueError("The in operator accepts at most 100 values.")
                placeholders = ", ".join("?" for _ in condition.value)
                conditions.append(f"{field_sql} IN ({placeholders})")
                source_dataset, source_field = resolved_fields[condition.field]
                field_type = schemas[source_dataset][source_field]
                parameters.extend(_coerce_filter_value(field_type, value) for value in condition.value)
            else:
                if isinstance(condition.value, (list, dict)):
                    raise ValueError("Filter values must be scalar, except for the in operator.")
                conditions.append(f"{field_sql} {sql_operators[condition.operator]} ?")
                source_dataset, source_field = resolved_fields[condition.field]
                field_type = schemas[source_dataset][source_field]
                parameters.append(_coerce_filter_value(field_type, condition.value))

        sql = f"SELECT {', '.join(select_parts)} FROM " + " ".join(from_parts)
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        if request.aggregations and request.group_by:
            sql += " GROUP BY " + ", ".join(
                _qualified(resolved_fields[field]) for field in request.group_by
            )
        if request.order_by:
            order_sql = [
                f"{_quote(item.field)} {'DESC' if item.direction == 'desc' else 'ASC'}"
                for item in request.order_by
            ]
            sql += " ORDER BY " + ", ".join(order_sql)
        sql += " LIMIT ?"
        parameters.append(request.limit + 1)

        try:
            with duckdb.connect() as connection:
                cursor = connection.execute(sql, parameters)
                names = [column[0] for column in cursor.description]
                fetched = cursor.fetchall()
        except duckdb.Error as error:
            raise ValueError("The Gold query could not be run; check filter values against field types.") from error

        truncated = len(fetched) > request.limit
        rows = [
            {name: _json_value(value) for name, value in zip(names, row)}
            for row in fetched[: request.limit]
        ]
        return {
            "dataset": dataset.name,
            "columns": names,
            "rows": rows,
            "row_count": len(rows),
            "limit": request.limit,
            "truncated": truncated,
        }

    def _get_dataset(self, name: str) -> Dataset:
        try:
            return DATASETS[name]
        except KeyError as error:
            raise KeyError(name) from error

    def _path(self, name: str) -> Path:
        return self.gold_dir / f"{name}.parquet"

    def _field_types(self, name: str) -> dict[str, str]:
        details = self.dataset_details(name)
        return {field["name"]: field["type"] for field in details["fields"]}


def _quote(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _resolve_field(reference: str, schemas: dict[str, dict[str, str]]) -> tuple[str, str]:
    if "." in reference:
        dataset_name, field_name = reference.split(".", 1)
        if dataset_name not in schemas or field_name not in schemas[dataset_name]:
            raise ValueError(f"Unknown field: {reference}")
        return dataset_name, field_name

    matches = [dataset_name for dataset_name, fields in schemas.items() if reference in fields]
    if not matches:
        raise ValueError(f"Unknown field: {reference}")
    if len(matches) > 1:
        raise ValueError(f"Ambiguous field '{reference}'; qualify it with a dataset name.")
    return matches[0], reference


def _qualified(field: tuple[str, str]) -> str:
    dataset_name, field_name = field
    return f"{_quote(dataset_name)}.{_quote(field_name)}"


def _is_numeric(field_type: str) -> bool:
    return any(kind in field_type.upper() for kind in ("INT", "FLOAT", "DOUBLE", "DECIMAL", "NUMERIC"))


def _coerce_filter_value(field_type: str, value: Any) -> Any:
    if "DATE" in field_type.upper() and isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError as error:
            raise ValueError("Date filters must use YYYY-MM-DD format.") from error
    return value


def _json_value(value: Any) -> Any:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    return value
