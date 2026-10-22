"""
Pytest configuration and shared fixtures for Olist EDA data tests.
"""

from pathlib import Path
import pandas as pd
import pytest

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PACKAGE_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"


@pytest.fixture(scope="session")
def raw_data_dir() -> Path:
    return RAW_DIR


@pytest.fixture(scope="session")
def processed_data_dir() -> Path:
    return PROCESSED_DIR


@pytest.fixture(scope="session")
def order_items_df() -> pd.DataFrame:
    csv_path = RAW_DIR / "order_items.csv"
    assert csv_path.exists(), f"Missing file: {csv_path}"
    return pd.read_csv(csv_path)


@pytest.fixture(scope="session")
def products_df() -> pd.DataFrame:
    csv_path = RAW_DIR / "products.csv"
    assert csv_path.exists(), f"Missing file: {csv_path}"
    return pd.read_csv(csv_path)


@pytest.fixture(scope="session")
def orders_df() -> pd.DataFrame:
    csv_path = RAW_DIR / "orders.csv"
    assert csv_path.exists(), f"Missing file: {csv_path}"
    return pd.read_csv(csv_path)


@pytest.fixture(scope="session")
def integrated_clean_df() -> pd.DataFrame:
    csv_path = PROCESSED_DIR / "ecommerce_integrated_clean.csv"
    assert csv_path.exists(), f"Missing file: {csv_path}"
    df = pd.read_csv(csv_path)
    # Parse timestamps for downstream date tests
    time_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in time_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df
