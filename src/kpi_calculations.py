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


def compute_yoy_badges_data(
    data: pd.DataFrame, *, max_years: int = 3
) -> list[dict]:
    """Return structured data for YoY badges for up to `max_years`."""
    if data.empty:
        return []

    monthly = (
        data.groupby(data["Date"].dt.to_period("M"))["Amount"]
        .sum()
        .sort_index()
    )
    if monthly.empty:
        return []

    years_ordered = sorted(set(monthly.index.year))
    results: list[dict] = []
    seen = 0

    for yr in reversed(years_ordered):
        if seen >= max_years:
            break

        year_months = monthly[monthly.index.year == yr]
        if year_months.empty:
            continue

        last_month = int(year_months.index.month.max())
        current_rev = monthly[
            (monthly.index.year == yr) & (monthly.index.month <= last_month)
        ].sum()
        prior_rev = monthly[
            (monthly.index.year == yr - 1) & (monthly.index.month <= last_month)
        ].sum()

        if prior_rev == 0:
            results.append(
                {
                    "year": int(yr),
                    "pct": None,
                    "direction": "neutral",
                }
            )
        else:
            pct = (current_rev - prior_rev) / prior_rev * 100
            direction = "positive" if pct >= 0 else "negative"
            results.append(
                {
                    "year": int(yr),
                    "pct": float(pct),
                    "direction": direction,
                }
            )

        seen += 1

    return results


def compute_mom_badges_data(
    data: pd.DataFrame, *, max_months: int = 3
) -> list[dict]:
    """Return structured data for MoM badges for up to `max_months`."""
    if data.empty:
        return []

    monthly = (
        data.groupby(data["Date"].dt.to_period("M"))["Amount"]
        .sum()
        .sort_index()
    )
    if len(monthly) < 2:
        return []

    periods = list(monthly.index)
    results: list[dict] = []

    # Walk backwards and collect up to `max_months` valid pairs
    for idx in range(len(periods) - 1, -1, -1):
        if len(results) >= max_months:
            break
        if idx == 0:
            continue

        current_period = periods[idx]
        prior_period = periods[idx - 1]
        current_rev = monthly.loc[current_period]
        prior_rev = monthly.loc[prior_period]

        label = current_period.strftime("%b %Y")

        if prior_rev == 0:
            results.append(
                {
                    "label": label,
                    "pct": None,
                    "direction": "neutral",
                }
            )
        else:
            pct = (current_rev - prior_rev) / prior_rev * 100
            direction = "positive" if pct >= 0 else "negative"
            results.append(
                {
                    "label": label,
                    "pct": float(pct),
                    "direction": direction,
                }
            )

    # We built from latest backwards, so reverse to chronological
    results.reverse()
    return results
