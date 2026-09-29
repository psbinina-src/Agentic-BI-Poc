"""Deterministic, in-memory synthetic e-commerce source generation."""

from __future__ import annotations

import random
from datetime import date, timedelta
from decimal import Decimal

from p1_u1.config import GeneratorConfig
from p1_u1.models import (
    Customer,
    InventorySnapshot,
    OrderHeader,
    OrderLine,
    Product,
    SourceDataset,
)

REGIONS = ("North", "South", "East", "West", "Central")
SEGMENTS = ("Standard", "Plus", "Premium")
CHANNELS = ("Online", "Retail", "Marketplace")
ACQUISITION_CHANNELS = ("Search", "Referral", "Social", "Direct")
PAYMENT_METHODS = ("Card", "Wallet", "Transfer")
CATEGORY_SUBCATEGORIES = {
    "Electronics": ("Audio", "Computing", "Accessories"),
    "Home": ("Kitchen", "Decor", "Storage"),
    "Outdoor": ("Fitness", "Garden", "Travel"),
    "Apparel": ("Basics", "Activewear", "Outerwear"),
}


def _day_offset(rng: random.Random, days: int) -> int:
    return rng.randrange(days + 1)


def generate_dataset(config: GeneratorConfig) -> SourceDataset:
    """Build a complete source dataset in memory using deterministic rules."""
    rng = random.Random(config.seed)
    day_count = (config.end_date - config.start_date).days + 1
    dataset = SourceDataset()
    region_index_by_customer: dict[str, int] = {}

    # Stable, synthetic customer profiles. The first 10% form a repeat-purchase cohort.
    repeat_customer_count = max(1, min(config.customer_count, config.customer_count // 10))
    customer_first_orders: dict[str, date] = {}
    for index in range(1, config.customer_count + 1):
        customer_id = f"CUST-{index:06d}"
        first_order = config.start_date + timedelta(days=_day_offset(rng, day_count - 1))
        customer_first_orders[customer_id] = first_order
        region_index_by_customer[customer_id] = (index - 1) % len(REGIONS)
        dataset.customers.append(
            Customer(
                customer_id=customer_id,
                customer_name=f"Customer {index:06d}",
                customer_segment=SEGMENTS[(index - 1) % len(SEGMENTS)],
                region=REGIONS[(index - 1) % len(REGIONS)],
                acquisition_channel=ACQUISITION_CHANNELS[(index - 1) % len(ACQUISITION_CHANNELS)],
                acquisition_date=config.start_date + timedelta(days=_day_offset(rng, max(0, (first_order - config.start_date).days))),
                customer_status="Active" if index % 20 else "Inactive",
            )
        )

    # Product cohorts are stable. The first products have high velocity and low stock.
    low_stock_cohort_size = max(1, min(config.product_count, config.product_count // 20))
    product_categories: dict[str, tuple[str, int]] = {}
    for index in range(1, config.product_count + 1):
        product_id = f"PROD-{index:06d}"
        category = tuple(CATEGORY_SUBCATEGORIES)[(index - 1) % len(CATEGORY_SUBCATEGORIES)]
        subcategories = CATEGORY_SUBCATEGORIES[category]
        reorder_point = 20 + (index % 31)
        product_categories[product_id] = (category, reorder_point)
        dataset.products.append(
            Product(
                product_id=product_id,
                product_name=f"Product {index:06d}",
                category=category,
                subcategory=subcategories[(index - 1) % len(subcategories)],
                list_price=Decimal(5 + (index * 7 % 196)).quantize(Decimal("0.01")),
                reorder_point=reorder_point,
                product_status="Active" if index % 50 else "Discontinued",
            )
        )

    # Create exactly the requested order lines, then derive each header from its lines.
    orders_by_id: dict[str, OrderHeader] = {}
    line_counter = 0
    order_counter = 0
    while line_counter < config.order_line_count:
        order_counter += 1
        order_id = f"ORD-{order_counter:07d}"
        if order_counter <= 2:
            customer_index = 1
        elif order_counter <= repeat_customer_count * 3:
            customer_index = ((order_counter - 1) % repeat_customer_count) + 1
        else:
            customer_index = rng.randrange(1, config.customer_count + 1)
        customer_id = f"CUST-{customer_index:06d}"
        first_order = customer_first_orders[customer_id]
        earliest = max(config.start_date, first_order)
        available_days = (config.end_date - earliest).days
        order_date = earliest + timedelta(days=_day_offset(rng, available_days))
        month_wave = 1 + (order_date.month % 4) * 0.18
        order_status = "Completed" if order_counter % 10 != 0 else "Cancelled"
        header = OrderHeader(
            order_id=order_id,
            customer_id=customer_id,
            order_date=order_date,
            order_status=order_status,
            payment_method=PAYMENT_METHODS[(order_counter - 1) % len(PAYMENT_METHODS)],
            channel=CHANNELS[(order_counter - 1) % len(CHANNELS)],
        )
        orders_by_id[order_id] = header

        lines_for_order = 1 if order_counter <= 2 else 1 + rng.randrange(3)
        for _ in range(lines_for_order):
            if line_counter >= config.order_line_count:
                break
            line_counter += 1
            # Deterministic scenario assignment: first 10% of products are high-velocity.
            if line_counter <= min(config.product_count, 2):
                product_index = line_counter
            elif line_counter % 3 != 0:
                product_index = ((line_counter - 1) % low_stock_cohort_size) + 1
            else:
                product_index = rng.randrange(1, config.product_count + 1)
            product_id = f"PROD-{product_index:06d}"
            category_index = (product_index - 1) % len(CATEGORY_SUBCATEGORIES)
            category_multiplier = 1.0 + category_index * 0.12
            region_demand = region_index_by_customer[customer_id] % 3
            if product_index <= low_stock_cohort_size:
                quantity = max(25, dataset.products[product_index - 1].reorder_point) + (line_counter % 5) + region_demand
            else:
                quantity = 1 + (line_counter % 3) + region_demand
            unit_price = dataset.products[product_index - 1].list_price
            discount_rate = Decimal((line_counter % 16) / 100).quantize(Decimal("0.01"))
            dataset.order_lines.append(
                OrderLine(
                    order_line_id=f"LINE-{line_counter:07d}",
                    order_id=order_id,
                    product_id=product_id,
                    quantity=quantity,
                    unit_price=(unit_price * Decimal(str(category_multiplier * month_wave))).quantize(Decimal("0.01")),
                    discount_rate=discount_rate,
                )
            )

    dataset.orders.extend(orders_by_id.values())
    dataset.orders.sort(key=lambda item: item.order_id)

    # Daily snapshots for each product/day. High-velocity cohort has a guaranteed
    # stockout/at-reorder example in the final snapshot.
    current_day = config.start_date
    while current_day <= config.end_date:
        day_index = (current_day - config.start_date).days
        for product_index in range(1, config.product_count + 1):
            product_id = f"PROD-{product_index:06d}"
            _, reorder_point = product_categories[product_id]
            if product_index <= low_stock_cohort_size and current_day == config.end_date:
                on_hand = max(0, reorder_point - 1)
            elif product_index <= low_stock_cohort_size:
                on_hand = reorder_point + (day_index * 3 + product_index) % 40
            else:
                on_hand = reorder_point + 10 + (day_index + product_index * 7) % 90
            dataset.inventory_snapshots.append(
                InventorySnapshot(
                    snapshot_date=current_day,
                    product_id=product_id,
                    inventory_on_hand=on_hand,
                    reorder_point=reorder_point,
                )
            )
        current_day += timedelta(days=1)

    return dataset
