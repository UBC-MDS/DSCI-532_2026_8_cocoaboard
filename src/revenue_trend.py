"""Revenue trend line chart for top 5 salespersons."""

import pandas as pd
import altair as alt
from shiny import ui


def revenue_trend_ui():
    """Build the revenue trend card."""
    return ui.card(
        ui.card_header("Revenue Trend — Top 5 Sales Reps"),
        ui.output_ui("revenue_trend_chart"),
        full_screen=True,
        class_="card-bg-white",
    )


def revenue_trend_chart_ui(data: pd.DataFrame):
    """Build the revenue trend line chart UI (iframe or empty message)."""
    if data is None or data.empty:
        return ui.p("No data to display.")

    top5 = (
        data.groupby("Sales Person")["Amount"]
        .sum()
        .nlargest(5)
        .index.tolist()
    )
    trend_data = data[data["Sales Person"].isin(top5)].copy()
    trend_data["Month"] = trend_data["Date"].dt.to_period("M").dt.to_timestamp()

    monthly = (
        trend_data.groupby(["Month", "Sales Person"])["Amount"]
        .sum()
        .reset_index()
    )

    chart = (
        alt.Chart(monthly)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "Month:T",
                title="Month",
                timeUnit="yearmonth",
                axis=alt.Axis(tickCount="month", format="%b %Y", labelAngle=-45),
            ),
            y=alt.Y("Amount:Q", title="Revenue (USD)", axis=alt.Axis(format="$,.0f")),
            color=alt.Color(
                "Sales Person:N",
                title="Sales Rep",
                scale=alt.Scale(
                    range=["#E63946", "#1D8CD6", "#2ECC71", "#9B59B6", "#F39C12"]
                ),
            ),
            tooltip=[
                alt.Tooltip("Sales Person:N", title="Sales Rep"),
                alt.Tooltip("Month:T", title="Month", format="%b %Y"),
                alt.Tooltip("Amount:Q", title="Revenue", format="$,.0f"),
            ],
        )
        .properties(width="container")
    )

    return ui.tags.iframe(
        srcdoc=chart.to_html(),
        style="width:100%;height:400px;border:none;",
    )
