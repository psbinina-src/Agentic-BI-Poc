"""Source dataset validation and deterministic scenario checks."""

from __future__ import annotations

from collections import Counter
from datetime import date

from p1_u1.config import GeneratorConfig
from p1_u1.models import SourceDataset, ValidationIssue, ValidationReport

ALLOWED_SEGMENTS = {"Standard", "Plus", "Premium"}
ALLOWED_REGIONS = {"North", "South", "East", "West", "Central"}
ALLOWED_ORDER_STATUSES = {"Completed", "Cancelled"}
ALLOWED_CHANNELS = {"Online", "Retail", "Marketplace"}


def validate_dataset(dataset: SourceDataset, config: GeneratorConfig) -> ValidationReport:
    """Validate entity counts, identifiers, relationships, domains, and scenarios."""
    issues: list[ValidationIssue] = []

    if len(dataset.customers) != config.customer_count:
        issues.append(ValidationIssue("customer_count", "customer count does not match configuration", "customers"))
    if len(dataset.products) != config.product_count:
        issues.append(ValidationIssue("product_count", "product count does not match configuration", "products"))
    if len(dataset.order_lines) != config.order_line_count:
        issues.append(ValidationIssue("order_line_count", "order-line count does not match configuration", "order_lines"))
    if len(dataset.inventory_snapshots) != config.inventory_snapshot_count:
        issues.append(ValidationIssue("inventory_count", "inventory snapshot count does not match configuration", "inventory_snapshots"))

    customer_ids = [item.customer_id for item in dataset.customers]
    product_ids = [item.product_id for item in dataset.products]
    order_ids = [item.order_id for item in dataset.orders]
    line_ids = [item.order_line_id for item in dataset.order_lines]
    if len(customer_ids) != len(set(customer_ids)):
        issues.append(ValidationIssue("duplicate_customer_id", "customer IDs must be unique", "customers"))
    if len(product_ids) != len(set(product_ids)):
        issues.append(ValidationIssue("duplicate_product_id", "product IDs must be unique", "products"))
    if len(order_ids) != len(set(order_ids)):
        issues.append(ValidationIssue("duplicate_order_id", "order IDs must be unique", "orders"))
    if len(line_ids) != len(set(line_ids)):
        issues.append(ValidationIssue("duplicate_order_line_id", "order-line IDs must be unique", "order_lines"))

    customer_set = set(customer_ids)
    product_set = set(product_ids)
    order_by_id = {item.order_id: item for item in dataset.orders}
    line_counts: Counter[str] = Counter()
    product_sales: Counter[str] = Counter()
    completed_order_ids = {order.order_id for order in dataset.orders if order.order_status == "Completed"}
    for order in dataset.orders:
        if order.customer_id not in customer_set:
            issues.append(ValidationIssue("unknown_order_customer", f"unknown customer {order.customer_id}", "orders"))
        if order.order_status not in ALLOWED_ORDER_STATUSES:
            issues.append(ValidationIssue("invalid_order_status", f"invalid status {order.order_status}", "orders"))
        if order.channel not in ALLOWED_CHANNELS:
            issues.append(ValidationIssue("invalid_channel", f"invalid channel {order.channel}", "orders"))
        if not config.start_date <= order.order_date <= config.end_date:
            issues.append(ValidationIssue("order_date_range", "order date is outside the configured range", "orders"))

    for line in dataset.order_lines:
        if line.order_id not in order_by_id:
            issues.append(ValidationIssue("unknown_order", f"unknown order {line.order_id}", "order_lines"))
        else:
            line_counts[line.order_id] += 1
        if line.product_id not in product_set:
            issues.append(ValidationIssue("unknown_product", f"unknown product {line.product_id}", "order_lines"))
        if line.quantity <= 0:
            issues.append(ValidationIssue("invalid_quantity", "quantity must be positive", "order_lines"))
        if line.unit_price < 0 or line.discount_rate < 0 or line.discount_rate > 1:
            issues.append(ValidationIssue("invalid_price_or_discount", "price and discount must be within the valid domain", "order_lines"))
        if line.order_id in completed_order_ids:
            product_sales[line.product_id] += line.quantity

    for order in dataset.orders:
        if line_counts[order.order_id] < 1:
            issues.append(ValidationIssue("empty_order", f"order {order.order_id} has no lines", "orders"))

    seen_inventory: set[tuple[date, str]] = set()
    low_stock_product_ids: set[str] = set()
    last_day = config.end_date
    reorder_by_product = {item.product_id: item.reorder_point for item in dataset.products}
    for snapshot in dataset.inventory_snapshots:
        key = (snapshot.snapshot_date, snapshot.product_id)
        if key in seen_inventory:
            issues.append(ValidationIssue("duplicate_inventory_key", f"duplicate snapshot {key}", "inventory_snapshots"))
        seen_inventory.add(key)
        if snapshot.product_id not in product_set:
            issues.append(ValidationIssue("unknown_inventory_product", f"unknown product {snapshot.product_id}", "inventory_snapshots"))
        if not config.start_date <= snapshot.snapshot_date <= config.end_date:
            issues.append(ValidationIssue("snapshot_date_range", "snapshot date is outside the configured range", "inventory_snapshots"))
        if snapshot.inventory_on_hand < 0 or snapshot.reorder_point < 0:
            issues.append(ValidationIssue("negative_inventory", "inventory and reorder point must be nonnegative", "inventory_snapshots"))
        if snapshot.snapshot_date == last_day and snapshot.inventory_on_hand <= snapshot.reorder_point:
            low_stock_product_ids.add(snapshot.product_id)

    customer_region_by_id = {customer.customer_id: customer.region for customer in dataset.customers}
    product_category_by_id = {product.product_id: product.category for product in dataset.products}
    order_regions = {
        customer_region_by_id[order.customer_id]
        for order in dataset.orders
        if order.customer_id in customer_region_by_id
    }
    sold_categories = {
        product_category_by_id[line.product_id]
        for line in dataset.order_lines
        if line.product_id in product_category_by_id
    }
    scenarios = {
        "repeat_purchasing": any(count > 1 for count in Counter(order.customer_id for order in dataset.orders).values()),
        "time_region_category_variation": (config.start_date == config.end_date or len({order.order_date for order in dataset.orders}) > 1)
        and len(order_regions) > 1
        and len(sold_categories) > 1,
        "low_stock_with_sales_velocity": any(
            product_id in low_stock_product_ids
            and quantity >= max(5, reorder_by_product.get(product_id, 0))
            for product_id, quantity in product_sales.items()
        ),
    }
    for scenario, passed in scenarios.items():
        if not passed:
            issues.append(ValidationIssue("scenario_missing", f"required scenario not present: {scenario}"))

    for customer in dataset.customers:
        if customer.customer_segment not in ALLOWED_SEGMENTS or customer.region not in ALLOWED_REGIONS:
            issues.append(ValidationIssue("invalid_customer_domain", f"invalid profile values for {customer.customer_id}", "customers"))
        if customer.acquisition_date > config.end_date:
            issues.append(ValidationIssue("invalid_acquisition_date", f"acquisition date after configured end for {customer.customer_id}", "customers"))

    return ValidationReport(issues=tuple(issues), scenarios=scenarios)
