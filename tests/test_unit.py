"""Unit tests for CocoaBoard pure data-transformation functions.

These tests verify isolated function behavior with explicit inputs and expected outputs.
Run with: pytest tests/test_unit.py
"""

import pandas as pd
import pytest

from src.leaderboard import leaderboard_table_data
from src.map_chart import _inject_click_handler, _IIFE_MARKER, _MAP_CLICK_JS
from src.kpi_calculations import compute_yoy_revenue, compute_mom_revenue


# ── leaderboard_table_data ────────────────────────────────────────────────────


def test_leaderboard_empty_returns_correct_schema(empty_df):
    """Empty input yields a DataFrame with all expected column headers; any schema
    change would break downstream rendering in the Shiny DataGrid component."""
    result = leaderboard_table_data(empty_df)
    expected_cols = ["Rank", "Sales Rep", "Revenue", "Transactions", "Boxes", "Avg Deal", "Rev Share"]
    assert list(result.columns) == expected_cols
    assert len(result) == 0


def test_leaderboard_ranks_by_revenue_descending(sample_df):
    """Reps are sorted by total revenue descending so the top earner is always rank 1;
    a sort-direction bug would silently flip the leaderboard."""
    result = leaderboard_table_data(sample_df)
    reps = result.iloc[:-1]  # exclude summary row
    assert reps.iloc[0]["Sales Rep"] == "Alice"   # Alice: $5,000
    assert reps.iloc[1]["Sales Rep"] == "Bob"     # Bob:   $1,500
    assert list(reps["Rank"]) == [1, 2]


def test_leaderboard_summary_row_shows_totals(sample_df):
    """The final row must aggregate all reps into a 'AVERAGE / TOTAL' summary;
    a missing summary row would break the leaderboard footer display."""
    result = leaderboard_table_data(sample_df)
    summary = result.iloc[-1]
    assert summary["Sales Rep"] == "AVERAGE / TOTAL"
    assert summary["Revenue"] == "$6,500"
    assert summary["Rev Share"] == "100.0%"


def test_leaderboard_rev_shares_sum_to_100(sample_df):
    """Individual rev shares must sum to 100 % so the footer is consistent;
    a rounding or division error could cause shares to drift above or below 100."""
    result = leaderboard_table_data(sample_df)
    reps = result.iloc[:-1]  # exclude summary
    total = sum(float(r.strip("%")) for r in reps["Rev Share"])
    assert abs(total - 100.0) < 0.2  # allow ±0.2 for display rounding


# ── _inject_click_handler ─────────────────────────────────────────────────────


def test_inject_click_handler_inserts_js_block():
    """The click-handler injection must insert the postMessage JS before the Vega IIFE;
    without it, map clicks cannot propagate country names to the Shiny server."""
    html = f"<head></head><body>{_IIFE_MARKER}</body>"
    result = _inject_click_handler(html)
    assert _MAP_CLICK_JS in result


def test_inject_click_handler_preserves_iife_marker():
    """The IIFE marker must remain in the output after injection so Vega still
    renders the chart; losing the marker would produce broken chart HTML."""
    html = f"<head></head><body>{_IIFE_MARKER}</body>"
    result = _inject_click_handler(html)
    assert _IIFE_MARKER in result


def test_inject_click_handler_noop_on_missing_marker():
    """HTML that does not contain the IIFE marker must pass through unchanged;
    mis-injecting into arbitrary HTML would corrupt unrelated markup."""
    html = "<html><body>no marker here</body></html>"
    result = _inject_click_handler(html)
    assert result == html


# ── compute_yoy_revenue ───────────────────────────────────────────────────────


def test_compute_yoy_revenue_empty_returns_na(empty_df):
    """Empty data must return 'N/A' instead of raising a ZeroDivisionError;
    this guards the KPI box when all active filters produce no rows."""
    assert compute_yoy_revenue(empty_df) == "N/A"


def test_compute_yoy_revenue_positive_growth(two_year_df):
    """YoY returns '+100.0%' when revenue exactly doubles year-over-year;
    an incorrect formula (e.g. swapped numerator/denominator) would flip the sign."""
    # 2022 Jan–Feb: 100+200=300; 2023 Jan–Feb: 200+400=600 → (600-300)/300*100 = +100.0%
    assert compute_yoy_revenue(two_year_df) == "+100.0%"


def test_compute_yoy_revenue_single_year_returns_na():
    """When only one calendar year of data is present, prior_rev is 0 and the function
    must return 'N/A' rather than divide by zero."""
    df = pd.DataFrame(
        {
            "Sales Person": ["Alice"],
            "Country": ["Australia"],
            "Product": ["Dark Bars"],
            "Date": pd.to_datetime(["2022-06-15"]),
            "Amount": [1000.0],
            "Boxes Shipped": [100],
        }
    )
    assert compute_yoy_revenue(df) == "N/A"


# ── compute_mom_revenue ───────────────────────────────────────────────────────


def test_compute_mom_revenue_empty_returns_na(empty_df):
    """Empty data must return 'N/A' without raising an exception;
    guards the MoM KPI box when all filters produce no matching rows."""
    assert compute_mom_revenue(empty_df) == "N/A"


def test_compute_mom_revenue_single_month_returns_na(single_month_df):
    """With only one month of data there is no prior month to compare, so the function
    must return 'N/A'; otherwise the MoM box would show a spurious percentage."""
    assert compute_mom_revenue(single_month_df) == "N/A"


def test_compute_mom_revenue_positive_growth(two_year_df):
    """MoM returns '+100.0%' when the last month's revenue doubles the prior month's;
    incorrect indexing (e.g. comparing wrong months) would return a wrong value."""
    # Monthly sorted: Jan-2022=100, Feb-2022=200, Jan-2023=200, Feb-2023=400
    # Current=Feb-2023=400, Prior=Jan-2023=200 → (400-200)/200*100 = +100.0%
    assert compute_mom_revenue(two_year_df) == "+100.0%"
