"""
Business Metrics and Analytical Aggregation Sanity Tests.

Verifies:
1. Revenue (GMV) calculations and market concentration thresholds.
2. Freight ratio disparity across budget vs premium pricing segments.
3. Logistics carrier SLA breach rates and delay magnitude parameters.
"""

import pandas as pd


def test_top10_categories_gmv_concentration(integrated_clean_df: pd.DataFrame):
    # Rule: Top 10 categories must account for >= 60% of total GMV (observed: 67.14%)
    total_gmv = integrated_clean_df["price"].sum()
    category_gmv = (
        integrated_clean_df.groupby("product_category_name")["price"]
        .sum()
        .sort_values(ascending=False)
    )
    top10_gmv = category_gmv.head(10).sum()
    top10_share = (top10_gmv / total_gmv) * 100

    assert top10_share >= 60.0, f"Expected Top 10 GMV share >= 60%, got {top10_share:.2f}%"
    assert top10_share <= 80.0, f"Unexpectedly high Top 10 GMV share: {top10_share:.2f}%"


def test_freight_disparity_between_price_tiers(integrated_clean_df: pd.DataFrame):
    # Rule: Low-cost products (< R$ 50) face higher logistics burden than premium items (> R$ 150)
    budget_items = integrated_clean_df[integrated_clean_df["price"] < 50]
    premium_items = integrated_clean_df[integrated_clean_df["price"] > 150]

    budget_mean_ratio = budget_items["freight_ratio"].mean()
    premium_mean_ratio = premium_items["freight_ratio"].mean()

    assert budget_mean_ratio > premium_mean_ratio, (
        f"Expected budget freight ratio ({budget_mean_ratio:.2f}%) > "
        f"premium freight ratio ({premium_mean_ratio:.2f}%)"
    )
    assert budget_mean_ratio >= 30.0, f"Expected budget freight ratio >= 30%, got {budget_mean_ratio:.2f}%"
    assert premium_mean_ratio <= 20.0, f"Expected premium freight ratio <= 20%, got {premium_mean_ratio:.2f}%"


def test_carrier_sla_delay_rate(integrated_clean_df: pd.DataFrame):
    # Rule: SLA breach rate is expected to be between 15% and 25% (observed: 18.61%)
    delay_count = (integrated_clean_df["delivery_delay_days"] > 0).sum()
    delay_rate = (delay_count / len(integrated_clean_df)) * 100
    assert 15.0 <= delay_rate <= 25.0, f"Expected SLA delay rate in 15-25% range, got {delay_rate:.2f}%"


def test_delayed_orders_positive_delay_days(integrated_clean_df: pd.DataFrame):
    # Delayed orders must have delivery_delay_days > 0 and mean around 8-12 days
    delayed_subset = integrated_clean_df[integrated_clean_df["delivery_delay_days"] > 0]
    assert (delayed_subset["delivery_delay_days"] > 0).all(), "Found non-positive delay days on delayed orders"

    mean_delay = delayed_subset["delivery_delay_days"].mean()
    assert 7.0 <= mean_delay <= 13.0, f"Expected mean delay in 7-13 days range, got {mean_delay:.2f} days"
