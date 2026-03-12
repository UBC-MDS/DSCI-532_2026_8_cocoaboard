"""Revenue by product pie chart for product-level analysis and best-seller identification."""

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
    """Build the revenue-by-product pie chart (uses filtered data: year, country, product)."""
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

    # Pie chart with a colorful palette; tooltips show revenue and share
    chart = (
        alt.Chart(by_product)
        .mark_arc(innerRadius=0, outerRadius=120)
        .encode(
            theta=alt.Theta("Amount:Q", stack=True),
            color=alt.Color(
                "Product:N",
                title="Product",
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
                sort=alt.EncodingSortField("Amount", op="sum", order="descending"),
            ),
            tooltip=[
                alt.Tooltip("Product:N", title="Product"),
                alt.Tooltip("Amount:Q", title="Revenue", format="$,.0f"),
                alt.Tooltip("Share:Q", title="Share (%)", format=".1f"),
            ],
        )
        .properties(width="container")
    )

    return ui.tags.iframe(
        srcdoc=chart.to_html(),
        style="width:100%;height:260px;border:none;",
    )
