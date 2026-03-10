"""World choropleth map: revenue by country."""

import pandas as pd
import altair as alt
from shiny import ui


def map_chart_ui():
    """Build the world map card."""
    return ui.card(
        ui.card_header("Sales by Country"),
        ui.output_ui("map_chart"),
        full_screen=True,
    )


def country_choropleth_ui(
    data: pd.DataFrame,
    country_codes: dict,
    world_topo_url: str,
    chart_height: int = 320,
    iframe_height: str = "350px",
):
    """
    Build a country revenue choropleth UI from transaction data.
    Returns ui.p if no data, else an iframe with the chart.
    """
    if data is None or data.empty:
        return ui.p("No data to display.")

    country_sales = (
        data.groupby("Country")["Amount"].sum().reset_index()
    )
    country_sales["id"] = country_sales["Country"].map(country_codes)

    topo = alt.topo_feature(world_topo_url, "countries")
    background = (
        alt.Chart(topo)
        .mark_geoshape(fill="#d3c4b4", stroke="white", strokeWidth=0.5)
        .project("naturalEarth1")
        .properties(width="container", height=chart_height)
    )
    sales_layer = (
        alt.Chart(topo)
        .mark_geoshape(stroke="white", strokeWidth=0.5)
        .encode(
            color=alt.Color(
                "Amount:Q",
                scale=alt.Scale(scheme="oranges"),
                legend=alt.Legend(title="Revenue (USD)"),
            ),
            tooltip=[
                alt.Tooltip("Country:N", title="Country"),
                alt.Tooltip("Amount:Q", format="$,.0f", title="Revenue"),
            ],
        )
        .transform_lookup(
            lookup="id",
            from_=alt.LookupData(country_sales, "id", ["Amount", "Country"]),
        )
        .project("naturalEarth1")
        .properties(width="container", height=chart_height)
    )
    chart = (background + sales_layer).configure_view(strokeWidth=0)
    return ui.tags.iframe(
        srcdoc=chart.to_html(),
        style=f"width:100%;height:{iframe_height};border:none;",
    )
