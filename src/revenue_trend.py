"""Revenue trend line chart for top 5 salespersons."""

from shiny import ui


def revenue_trend_ui():
    """Build the revenue trend card."""
    return ui.card(
        ui.card_header("Revenue Trend — Top 5 Sales Reps"),
        ui.output_ui("revenue_trend_chart"),
        full_screen=True,
    )
