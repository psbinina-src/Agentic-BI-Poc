from p4_dashboard.generate import build_dashboard_payload


def test_build_dashboard_payload_uses_gold_model() -> None:
    payload = build_dashboard_payload()

    assert "summary" in payload
    assert "semantic_view" in payload
    assert "revenue_by_region" in payload
    assert "sales_by_channel" in payload
    assert "inventory_risk" in payload

    assert payload["summary"]["net_sales"] >= 0
    assert payload["summary"]["total_orders"] >= 0
    assert payload["semantic_view"][0]["table"] in {"sales_gold", "customers_gold", "products_gold", "inventory_gold"}
