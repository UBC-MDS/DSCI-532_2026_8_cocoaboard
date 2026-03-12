"""Revenue by product horizontal bar chart for product-level analysis and best-seller identification."""

import pandas as pd
import altair as alt
from shiny import ui


def product_revenue_ui():
    """Build the revenue-by-product card."""
    return ui.card(
        ui.card_header("Revenue by Product"),
        ui.output_ui("product_revenue_chart"),
        full_screen=True,
        class_="card-bg-white",
    )


def product_revenue_chart_ui(data: pd.DataFrame):
    """Build the revenue-by-product area chart (uses filtered data: year, country, product)."""
    if data is None or data.empty:
        return ui.p("No data to display.")

    by_product = (
        data.groupby("Product")["Amount"]
        .sum()
        .reset_index()
        .sort_values("Amount", ascending=False)
    )
    total = by_product["Amount"].sum()
    by_product["Share"] = (by_product["Amount"] / total * 100).round(1)

    # Horizontal bar (area) chart: bar length encodes revenue
    bar_height = max(160, min(360, 26 * len(by_product)))
    chart = (
        alt.Chart(by_product)
        .mark_bar()
        .encode(
            y=alt.Y("Product:N", sort="-x", title="Product"),
            x=alt.X("Amount:Q", title="Revenue (USD)", axis=alt.Axis(format="$,.0f")),
            color=alt.Color(
                "Product:N",
                legend=None,
                scale=alt.Scale(
                    range=[
                        "#E63946",
                        "#457B9D",
                        "#2A9D8F",
                        "#E9C46A",
                        "#9B59B6",
                        "#F4A261",
                        "#2ECC71",
                        "#E76F51",
                        "#3A86FF",
                        "#06D6A0",
                    ]
                ),
            ),
            tooltip=[
                alt.Tooltip("Product:N", title="Product"),
                alt.Tooltip("Amount:Q", title="Revenue", format="$,.0f"),
                alt.Tooltip("Share:Q", title="Share (%)", format=".1f"),
            ],
        )
        .properties(width="container", height=bar_height)
    )

    return ui.tags.iframe(
        srcdoc=chart.to_html(),
        style="width:100%;height:350px;border:none;",
    )
