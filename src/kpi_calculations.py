"""KPI metric calculations: year-over-year and month-over-month revenue change.

Extracted from the Shiny server function so they can be tested in isolation.
"""

import pandas as pd


def compute_yoy_revenue(data: pd.DataFrame, *, year: int | None = None) -> str:
    """Compute year-over-year revenue change.

    If `year` is provided, compares that year vs the prior year using months up to the
    last available month in `year`. Otherwise, compares the most recent year vs prior.
    Returns a formatted percentage string or 'N/A'.
    """
    if data.empty:
        return "N/A"
    monthly = data.groupby(data["Date"].dt.to_period("M"))["Amount"].sum()
    last_date = data["Date"].max()
    current_year = int(year) if year is not None else last_date.year
    year_months = monthly[monthly.index.year == current_year]
    if year_months.empty:
        return "N/A"
    last_month = int(year_months.index.month.max())
    current_rev = monthly[
        (monthly.index.year == current_year) & (monthly.index.month <= last_month)
    ].sum()
    prior_rev = monthly[
        (monthly.index.year == current_year - 1) & (monthly.index.month <= last_month)
    ].sum()
    if prior_rev == 0:
        return "N/A"
    pct = (current_rev - prior_rev) / prior_rev * 100
    arrow = "+" if pct >= 0 else ""
    return f"{arrow}{pct:.1f}%"


def compute_mom_revenue(data: pd.DataFrame) -> str:
    """Compute month-over-month revenue change for the two most recent months.

    Compares the last available month's revenue to the prior month's revenue.
    Returns a formatted percentage string or 'N/A'.
    """
    if data.empty:
        return "N/A"
    monthly = data.groupby(data["Date"].dt.to_period("M"))["Amount"].sum().sort_index()
    if len(monthly) < 2:
        return "N/A"
    current_rev = monthly.iloc[-1]
    prior_rev = monthly.iloc[-2]
    if prior_rev == 0:
        return "N/A"
    pct = (current_rev - prior_rev) / prior_rev * 100
    arrow = "+" if pct >= 0 else ""
    return f"{arrow}{pct:.1f}%"
