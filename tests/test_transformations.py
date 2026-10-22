"""
Data Cleaning and Feature Engineering Transformation Tests.

Verifies:
1. Row count reconciliation (800 raw -> 763 clean integrated records).
2. Numerical validity and bounds of derived features.
3. Logical consistency of SLA delay indicators and delivery duration.
"""

import numpy as np
import pandas as pd


def test_row_count_reconciliation(integrated_clean_df: pd.DataFrame):
    # Cleansing filter criteria:
    # 1. 12 products with null categories removed
    # 2. 18 non-delivered orders removed
    # Net result: 800 items reduced to exactly 763 valid transactional items
    assert len(integrated_clean_df) == 763, f"Expected 763 rows, found {len(integrated_clean_df)}"


def test_no_null_critical_attributes(integrated_clean_df: pd.DataFrame):
    critical_cols = [
        "product_category_name",
        "price",
        "freight_value",
        "total_item_value",
        "freight_ratio",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in critical_cols:
        null_count = integrated_clean_df[col].isnull().sum()
        assert null_count == 0, f"Critical column {col} contains {null_count} null values"


def test_total_item_value_formula(integrated_clean_df: pd.DataFrame):
    # Rule: total_item_value == price + freight_value
    expected_totals = integrated_clean_df["price"] + integrated_clean_df["freight_value"]
    np.testing.assert_allclose(
        integrated_clean_df["total_item_value"].values,
        expected_totals.values,
        rtol=1e-5,
        err_msg="total_item_value mismatch against price + freight_value",
    )


def test_freight_ratio_bounds_and_formula(integrated_clean_df: pd.DataFrame):
    # Rule: freight_ratio == (freight_value / total_item_value) * 100
    expected_ratios = (
        integrated_clean_df["freight_value"] / integrated_clean_df["total_item_value"]
    ) * 100
    np.testing.assert_allclose(
        integrated_clean_df["freight_ratio"].values,
        expected_ratios.values,
        atol=0.01,
        err_msg="freight_ratio mismatch against mathematical formula",
    )
    # Bounds: must be between 0% and 100%
    assert (integrated_clean_df["freight_ratio"] > 0).all(), "Found negative freight ratio"
    assert (integrated_clean_df["freight_ratio"] < 100).all(), "Found freight ratio >= 100%"


def test_delivery_duration_logic(integrated_clean_df: pd.DataFrame):
    # Rule: delivery duration in days must be >= 0
    assert (integrated_clean_df["delivery_duration_days"] >= 0).all(), "Found delivery duration < 0 days"


def test_sla_delay_indicator_consistency(integrated_clean_df: pd.DataFrame):
    # If delivery_delay_days > 0, delivered date must exceed estimated date
    delayed_rows = integrated_clean_df[integrated_clean_df["delivery_delay_days"] > 0]
    assert len(delayed_rows) == 142, f"Expected 142 delayed rows, found {len(delayed_rows)}"
    for _, row in delayed_rows.iterrows():
        assert row["order_delivered_customer_date"] > row["order_estimated_delivery_date"], (
            f"Row marked delay > 0 but delivered {row['order_delivered_customer_date']} "
            f"<= estimated {row['order_estimated_delivery_date']}"
        )
