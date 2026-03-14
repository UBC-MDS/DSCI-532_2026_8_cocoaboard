"""Shared pytest fixtures for CocoaBoard tests."""

import pandas as pd
import pytest


@pytest.fixture
def sample_df():
    """Small in-memory DataFrame with two reps across two months for leaderboard tests.

    Alice totals $5,000 and Bob totals $1,500 (total $6,500).
    """
    return pd.DataFrame(
        {
            "Sales Person": ["Alice", "Alice", "Bob", "Bob"],
            "Country": ["Australia", "Australia", "UK", "India"],
            "Product": ["Dark Bars", "Milk Bars", "Dark Bars", "Dark Bars"],
            "Date": pd.to_datetime(
                ["2022-01-15", "2022-02-10", "2022-01-20", "2022-02-25"]
            ),
            "Amount": [3000.0, 2000.0, 1000.0, 500.0],
            "Boxes Shipped": [300, 200, 100, 50],
        }
    )


@pytest.fixture
def empty_df():
    """Empty DataFrame with the correct column schema for edge-case tests."""
    return pd.DataFrame(
        columns=["Sales Person", "Country", "Product", "Date", "Amount", "Boxes Shipped"]
    )


@pytest.fixture
def two_year_df():
    """DataFrame spanning two years (2022–2023) for YoY and MoM calculation tests.

    Monthly totals: Jan-2022=100, Feb-2022=200, Jan-2023=200, Feb-2023=400.
    Expected YoY: +100.0% (prior 300 → current 600).
    Expected MoM: +100.0% (Jan-2023 200 → Feb-2023 400).
    """
    return pd.DataFrame(
        {
            "Sales Person": ["Alice"] * 4,
            "Country": ["Australia"] * 4,
            "Product": ["Dark Bars"] * 4,
            "Date": pd.to_datetime(
                ["2022-01-15", "2022-02-20", "2023-01-15", "2023-02-20"]
            ),
            "Amount": [100.0, 200.0, 200.0, 400.0],
            "Boxes Shipped": [10, 20, 20, 40],
        }
    )


@pytest.fixture
def single_month_df():
    """DataFrame with only one month of data for the MoM edge-case test."""
    return pd.DataFrame(
        {
            "Sales Person": ["Alice", "Alice"],
            "Country": ["Australia", "Australia"],
            "Product": ["Dark Bars", "Milk Bars"],
            "Date": pd.to_datetime(["2022-01-10", "2022-01-25"]),
            "Amount": [500.0, 300.0],
            "Boxes Shipped": [50, 30],
        }
    )
