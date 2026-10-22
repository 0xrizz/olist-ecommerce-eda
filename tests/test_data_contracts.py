"""
Data Contract and Schema Integrity Tests.

Verifies:
1. Physical existence and non-zero byte size of raw CSV files.
2. Required schema attributes and column presence.
3. Primary Key and Composite Key uniqueness.
4. Foreign Key referential integrity across relational boundaries.
"""

from pathlib import Path
import pandas as pd


def test_raw_files_exist_and_non_empty(raw_data_dir: Path):
    expected_files = ["order_items.csv", "products.csv", "orders.csv"]
    for filename in expected_files:
        filepath = raw_data_dir / filename
        assert filepath.exists(), f"Raw dataset missing: {filepath}"
        assert filepath.stat().st_size > 1024, f"Dataset file too small: {filepath}"


def test_order_items_schema(order_items_df: pd.DataFrame):
    required_cols = [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "price",
        "freight_value",
    ]
    for col in required_cols:
        assert col in order_items_df.columns, f"Missing required column in order_items: {col}"
    assert len(order_items_df) == 800, f"Expected 800 rows, found {len(order_items_df)}"


def test_products_schema(products_df: pd.DataFrame):
    required_cols = [
        "product_id",
        "product_category_name",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]
    for col in required_cols:
        assert col in products_df.columns, f"Missing required column in products: {col}"
    assert len(products_df) == 679, f"Expected 679 rows, found {len(products_df)}"


def test_orders_schema(orders_df: pd.DataFrame):
    required_cols = [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in required_cols:
        assert col in orders_df.columns, f"Missing required column in orders: {col}"
    assert len(orders_df) == 790, f"Expected 790 rows, found {len(orders_df)}"


def test_composite_key_uniqueness_order_items(order_items_df: pd.DataFrame):
    # Rule: Composite Key (order_id, order_item_id) must be strictly unique
    duplicates = order_items_df.duplicated(subset=["order_id", "order_item_id"]).sum()
    assert duplicates == 0, f"Found {duplicates} duplicate composite keys in order_items"


def test_primary_key_uniqueness_products(products_df: pd.DataFrame):
    # Rule: product_id must be strictly unique
    assert products_df["product_id"].is_unique, "product_id is not unique in products.csv"


def test_primary_key_uniqueness_orders(orders_df: pd.DataFrame):
    # Rule: order_id must be strictly unique
    assert orders_df["order_id"].is_unique, "order_id is not unique in orders.csv"


def test_foreign_key_referential_integrity(
    order_items_df: pd.DataFrame,
    products_df: pd.DataFrame,
    orders_df: pd.DataFrame,
):
    # All product_ids in order_items must exist in products
    item_products = set(order_items_df["product_id"])
    product_pks = set(products_df["product_id"])
    unmatched_products = item_products - product_pks
    assert len(unmatched_products) == 0, f"Found unmatched product_ids: {unmatched_products}"

    # All order_ids in order_items must exist in orders
    item_orders = set(order_items_df["order_id"])
    order_pks = set(orders_df["order_id"])
    unmatched_orders = item_orders - order_pks
    assert len(unmatched_orders) == 0, f"Found unmatched order_ids: {unmatched_orders}"
