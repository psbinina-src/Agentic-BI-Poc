from __future__ import annotations

import json
import os
from typing import Any, Literal

import httpx
from openai import OpenAI
from pydantic import BaseModel, ConfigDict, Field, ValidationError


DEFAULT_PHASE2_URL = "http://127.0.0.1:8100"
DEFAULT_MODEL = "gpt-4o-mini"
MAX_QUERY_ROWS = 200


class ChartEncoding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field: str
    type: Literal["quantitative", "nominal", "temporal"]
    title: str | None


class ChartProposal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=100)
    mark: Literal["bar", "line", "point", "area"]
    encoding: ChartEncodings


class ChartEncodings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    x: ChartEncoding
    y: ChartEncoding
    color: ChartEncoding | None
    tooltip: ChartEncoding | None


class AgentAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answer: str = Field(min_length=1, max_length=500)
    insight: str = Field(min_length=1, max_length=500)
    chart: ChartProposal | None


SYSTEM_PROMPT = """You are a careful business intelligence assistant for a synthetic e-commerce Gold data model.
Use the supplied Phase 2 Gold catalogue and field metadata before querying.
Use query_gold_aggregate for bounded aggregate results only. Never request or return raw customer or product IDs.
Use only datasets and fields returned by metadata, and only catalogue-approved joins. Do not invent data,
fields, metrics, forecasts, or semantic definitions. The API exposes physical Gold fields and generic
aggregations, not governed metrics. Use net_sales_amount for net sales; sum it only when clearly relevant.
Sales questions may group by channel, region (join customers_gold), category/subcategory (join products_gold),
or order_date. For relative-time questions, first discover the available date window with min/max on the Gold
date field, anchor the requested period to the latest available Gold date (not today's date), and tell the user
when the data ends. For date trends, filter the period and order results ascending by the date dimension so
the bounded result covers the requested interval. Customer questions may group by customer_segment or region. Inventory questions use
inventory_gold and may join products_gold for category/name. Explain missing forecast data as unsupported.
Use exactly one aggregate query. Then return exactly one JSON object with keys answer, insight, chart. chart is null if no data
was queried or the request is unsupported; otherwise chart has title, mark (bar, line, point, area), and
encoding with required x, y, color, tooltip properties; set unused color or tooltip to null. Each encoding
value has field and type (quantitative, nominal, temporal). Every encoded field must exist in the aggregate result columns. Use x/y axes that suit the data,
for example temporal x and quantitative y for trends. Base every claim on the result rows and keep the insight
concise. Do not include SQL, code fences, or extra prose outside the JSON object."""


def _tool_definitions() -> list[dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": "query_gold_aggregate",
                "description": "Run a read-only aggregate query over Gold through the Phase 2 API. Never request row-level identifiers.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "dataset": {"type": "string", "enum": ["sales_gold", "customers_gold", "products_gold", "inventory_gold"]},
                        "joins": {"type": "array", "items": {"type": "string", "enum": ["sales_gold", "customers_gold", "products_gold", "inventory_gold"]}},
                        "group_by": {"type": "array", "items": {"type": "string"}},
                        "aggregations": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "field": {"type": "string"},
                                    "function": {"type": "string", "enum": ["sum", "avg", "min", "max", "count", "count_distinct"]},
                                },
                                "required": ["field", "function"],
                                "additionalProperties": False,
                            },
                        },
                        "order_by": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "field": {"type": "string"},
                                    "direction": {"type": "string", "enum": ["asc", "desc"]},
                                },
                                "required": ["field", "direction"],
                                "additionalProperties": False,
                            },
                        },
                        "filters": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "field": {"type": "string"},
                                    "operator": {"type": "string", "enum": ["eq", "ne", "gt", "gte", "lt", "lte"]},
                                    "value": {"anyOf": [{"type": "string"}, {"type": "number"}, {"type": "boolean"}]},
                                },
                                "required": ["field", "operator", "value"],
                                "additionalProperties": False,
                            },
                        },
                        "limit": {"type": "integer", "minimum": 1, "maximum": MAX_QUERY_ROWS},
                    },
                    "required": ["dataset", "joins", "group_by", "aggregations", "order_by", "filters", "limit"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        },
    ]


class Phase3Agent:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        phase2_url: str | None = None,
        openai_client: Any | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        self.api_key = api_key if api_key is not None else os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
        self.phase2_url = (phase2_url or os.getenv("PHASE2_API_URL", DEFAULT_PHASE2_URL)).rstrip("/")
        self.openai_client = openai_client
        self.http_client = http_client or httpx.Client(timeout=15.0)

    def close(self) -> None:
        self.http_client.close()

    def answer(self, prompt: str) -> dict[str, Any]:
        if not self.api_key and self.openai_client is None:
            raise RuntimeError("OPENAI_API_KEY is not configured. Set it in your local environment and restart the service.")
        if not prompt.strip():
            raise ValueError("Enter a business question to analyze.")
        if len(prompt) > 1000:
            raise ValueError("Questions must be 1000 characters or fewer.")

        client = self.openai_client or OpenAI(api_key=self.api_key, timeout=45.0, max_retries=0)
        metadata = self._discover_metadata()
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": f"{SYSTEM_PROMPT}\n\nPhase 2 Gold catalogue and field metadata:\n{json.dumps(metadata, ensure_ascii=False)}"},
            {"role": "user", "content": prompt.strip()},
        ]
        query_completion = client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=_tool_definitions(),
            tool_choice={"type": "function", "function": {"name": "query_gold_aggregate"}},
            parallel_tool_calls=False,
            temperature=0,
        )
        assistant_message = query_completion.choices[0].message
        if len(assistant_message.tool_calls or []) != 1:
            raise RuntimeError("The agent did not produce exactly one Gold aggregate query. Try a more specific question.")

        tool_call = assistant_message.tool_calls[0]
        if tool_call.function.name != "query_gold_aggregate":
            raise RuntimeError("The agent requested an unsupported data operation.")
        try:
            query_arguments = json.loads(tool_call.function.arguments)
            latest_query = self._run_tool(tool_call.function.name, query_arguments)
        except (ValueError, KeyError, httpx.HTTPError, json.JSONDecodeError) as error:
            raise RuntimeError(f"The Gold query was rejected: {str(error)[:250]}") from error

        messages.append(assistant_message.model_dump(exclude_none=True))
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(latest_query, ensure_ascii=False, default=str),
        })
        answer_completion = client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "agentic_bi_answer",
                    "strict": True,
                    "schema": AgentAnswer.model_json_schema(),
                },
            },
            temperature=0,
        )
        answer_message = answer_completion.choices[0].message
        try:
            answer = AgentAnswer.model_validate_json(answer_message.content or "")
        except (ValidationError, ValueError) as error:
            raise RuntimeError("The AI response did not match the expected answer/chart format. Try a more specific question.") from error
        chart = self._build_vega_spec(answer.chart, latest_query)
        return {
            "answer": answer.answer,
            "insight": answer.insight,
            "chart": chart,
            "data": latest_query,
        }

    def _run_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name == "query_gold_aggregate":
            request = self._validate_query(arguments)
            result = self._post("/query", request)
            # Only aggregated rows are passed to OpenAI; never include raw fact/dimension records.
            return result
        raise ValueError("Unsupported agent tool.")

    def _discover_metadata(self) -> dict[str, Any]:
        catalog = self._get("/catalog")
        datasets = [
            item["name"]
            for item in catalog.get("datasets", [])
            if item.get("available") and item.get("name") in {"sales_gold", "customers_gold", "products_gold", "inventory_gold"}
        ]
        details = {name: self._get(f"/catalog/{name}") for name in datasets}
        return {"datasets": catalog.get("datasets", []), "relationships": catalog.get("relationships", []), "details": details}

    def _validate_query(self, arguments: dict[str, Any]) -> dict[str, Any]:
        allowed_datasets = {"sales_gold", "customers_gold", "products_gold", "inventory_gold"}
        dataset = arguments.get("dataset")
        if dataset not in allowed_datasets:
            raise ValueError("Unknown Gold dataset.")
        joins = arguments.get("joins", [])
        group_by = arguments.get("group_by", [])
        aggregations = arguments.get("aggregations", [])
        filters = arguments.get("filters", [])
        order_by = arguments.get("order_by", [])
        limit = arguments.get("limit", 20)
        if not isinstance(joins, list) or len(joins) > 2 or len(set(joins)) != len(joins):
            raise ValueError("Choose up to two unique documented Gold joins.")
        if not isinstance(group_by, list) or len(group_by) > 5 or not isinstance(aggregations, list) or not 1 <= len(aggregations) <= 5:
            raise ValueError("Aggregate queries require one to five measures and up to five grouping fields.")
        if not isinstance(filters, list) or len(filters) > 10:
            raise ValueError("Queries may contain at most ten filters.")
        if not isinstance(order_by, list) or len(order_by) > 5:
            raise ValueError("Queries may sort by at most five result fields.")
        if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= MAX_QUERY_ROWS:
            raise ValueError(f"Query limit must be between 1 and {MAX_QUERY_ROWS} rows.")

        catalog = self._get("/catalog")
        relationships = catalog.get("relationships", [])
        schema_by_dataset = {dataset: self._get(f"/catalog/{dataset}") for dataset in [dataset, *joins]}
        for joined_dataset in joins:
            if not any(
                relation["from_dataset"] == dataset and relation["to_dataset"] == joined_dataset
                for relation in relationships
            ):
                raise ValueError(f"The Gold catalogue does not document a join from {dataset} to {joined_dataset}.")

        fields: dict[str, dict[str, str]] = {}
        key_fields: set[str] = set()
        for dataset_name, details in schema_by_dataset.items():
            key_fields.update(f"{dataset_name}.{key}" for key in details.get("key_fields", []))
            for field in details.get("fields", []):
                fields[f"{dataset_name}.{field['name']}"] = {"type": field["type"], "dataset": dataset_name, "name": field["name"]}

        unqualified_names = {
            field["name"]
            for details in schema_by_dataset.values()
            for field in details.get("fields", [])
        }
        for field_name in unqualified_names:
            matches = [
                fields[f"{dataset_name}.{field_name}"]
                for dataset_name, details in schema_by_dataset.items()
                if any(field["name"] == field_name for field in details.get("fields", []))
            ]
            if len(matches) == 1:
                fields[field_name] = matches[0]

        def check_dimension(reference: str) -> dict[str, str]:
            if reference in key_fields or reference.rsplit(".", 1)[-1].endswith("_id"):
                raise ValueError("Identifier fields cannot be sent as chart dimensions or filters.")
            if reference not in fields:
                raise ValueError(f"Field '{reference}' was not found in the selected Gold dataset metadata.")
            return fields[reference]

        for dimension in group_by:
            check_dimension(dimension)
        for measure in aggregations:
            field = check_dimension_for_measure(measure, fields, key_fields, dataset)
            if measure["field"] not in fields:
                measure["field"] = f"{field['dataset']}.{field['name']}"
            function = measure.get("function")
            if function not in {"sum", "avg", "min", "max", "count", "count_distinct"}:
                raise ValueError("Unsupported aggregate function.")
            if function in {"sum", "avg"} and not _numeric(field["type"]):
                raise ValueError(f"{function} requires a numeric Gold field.")
            if function == "count_distinct" and f"{field['dataset']}.{field['name']}" not in key_fields:
                raise ValueError("count_distinct is only allowed for Gold key fields.")
        for condition in filters:
            field = check_dimension(condition.get("field", ""))
            value = condition.get("value")
            if isinstance(value, str) and len(value) > 100 or isinstance(value, list) and (not value or len(value) > 20):
                raise ValueError("Filter values must be short scalar values or lists of at most 20 items.")
            if isinstance(value, (dict, list)):
                raise ValueError("Filters must use scalar values.")
        result_fields = set(group_by)
        aggregate_aliases: dict[str, str | None] = {}
        for measure in aggregations:
            full_alias = f"{measure['function']}_{measure['field'].replace('.', '_')}"
            short_alias = f"{measure['function']}_{measure['field'].rsplit('.', 1)[-1]}"
            result_fields.add(full_alias)
            alias_variants = {short_alias, full_alias}
            measure_metadata = fields.get(measure["field"])
            if measure_metadata:
                qualified_alias = f"{measure['function']}_{measure_metadata['dataset']}_{measure_metadata['name']}"
                alias_variants.add(qualified_alias)
            for alias in alias_variants:
                if alias not in aggregate_aliases:
                    aggregate_aliases[alias] = full_alias
                elif aggregate_aliases[alias] != full_alias:
                    aggregate_aliases[alias] = None
        validated_order: list[dict[str, str]] = []
        for order in order_by:
            requested_field = order.get("field")
            if requested_field in aggregate_aliases and aggregate_aliases[requested_field]:
                order["field"] = aggregate_aliases[requested_field]
                requested_field = order["field"]
            if requested_field not in result_fields and isinstance(requested_field, str):
                suffix_matches = [
                    field
                    for field in result_fields
                    if field.rsplit(".", 1)[-1] == requested_field.rsplit(".", 1)[-1]
                ]
                if len(suffix_matches) == 1:
                    order["field"] = suffix_matches[0]
            if order.get("field") in result_fields and order.get("direction") in {"asc", "desc"}:
                validated_order.append(order)

        return {
            "dataset": dataset,
            "joins": joins,
            "group_by": group_by,
            "aggregations": aggregations,
            "order_by": validated_order,
            "filters": filters,
            "limit": min(limit, MAX_QUERY_ROWS),
        }

    def _build_vega_spec(self, chart: ChartProposal | None, query: dict[str, Any] | None) -> dict[str, Any] | None:
        if chart is None or query is None or not query.get("rows"):
            return None
        allowed_marks = {"bar", "line", "point", "area"}
        allowed_channels = {"x", "y", "color", "tooltip"}
        if chart.mark not in allowed_marks:
            raise RuntimeError("The generated chart uses an unsupported mark.")
        columns = set(query.get("columns", []))
        encoding: dict[str, Any] = {}
        for channel, definition in chart.encoding.model_dump(exclude_none=True).items():
            if channel not in allowed_channels or definition["field"] not in columns:
                raise RuntimeError("The generated chart references an unsupported channel or field.")
            if definition["type"] not in {"quantitative", "nominal", "temporal"}:
                raise RuntimeError("The generated chart uses an unsupported field type.")
            encoding[channel] = {"field": definition["field"], "type": definition["type"]}
            if definition.get("title"):
                encoding[channel]["title"] = definition["title"][:80]
        if not {"x", "y"}.issubset(encoding):
            raise RuntimeError("The generated chart must define x and y encodings.")
        return {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "data": {"values": query["rows"]},
            "mark": chart.mark,
            "encoding": encoding,
            "title": chart.title,
            "width": "container",
            "height": 320,
        }

    def _get(self, path: str) -> dict[str, Any]:
        response = self.http_client.get(f"{self.phase2_url}{path}")
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = self.http_client.post(f"{self.phase2_url}{path}", json=payload)
        response.raise_for_status()
        return response.json()


def check_dimension_for_measure(
    measure: dict[str, Any],
    fields: dict[str, dict[str, str]],
    key_fields: set[str],
    default_dataset: str | None = None,
) -> dict[str, str]:
    reference = measure.get("field", "")
    if reference not in fields and default_dataset and f"{default_dataset}.{reference}" in fields:
        reference = f"{default_dataset}.{reference}"
    if reference not in fields:
        raise ValueError(f"Field '{reference}' was not found in the selected Gold dataset metadata.")
    field = fields[reference]
    is_key = f"{field['dataset']}.{field['name']}" in key_fields
    if is_key and measure.get("function") not in {"count", "count_distinct"}:
        raise ValueError("Gold keys may only be used in count or distinct-count aggregates.")
    return field


def _numeric(field_type: str) -> bool:
    return any(token in field_type.upper() for token in ("INT", "FLOAT", "DOUBLE", "DECIMAL", "NUMERIC"))
