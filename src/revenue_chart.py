"""Revenue over time chart widget."""

import pandas as pd
import altair as alt
from shiny import ui


def revenue_chart_ui():
    """Build the revenue-over-time chart card UI."""
    return ui.layout_columns(
        ui.card(
            ui.card_header("Revenue Over Time"),
            ui.output_ui("revenue_chart"),
        ),
        col_widths=(12,),
        fill=False,
        fillable=False,
    )


def build_chart(monthly: pd.DataFrame):
    """Build Altair line chart from monthly revenue data. Returns HTML string."""
    chart = (
        alt.Chart(monthly)
        .mark_line(point=True, color="#5D3A1A", strokeWidth=2)
        .encode(
            x=alt.X("Month:T", title="Date"),
            y=alt.Y("Amount:Q", title="Revenue (USD)"),
            tooltip=["Month:T", "Amount:Q"],
        )
        .properties(width="container", height=300)
        .configure(background="#FFFEFB")
        .configure_axis(labelColor="#2C1810", titleColor="#5D3A1A")
        .configure_view(strokeWidth=0)
    )
    return ui.HTML(chart.to_html())
