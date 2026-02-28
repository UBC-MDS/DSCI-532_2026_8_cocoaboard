"""World choropleth map: revenue by country."""

from shiny import ui


def map_chart_ui():
    """Build the world map card."""
    return ui.card(
        ui.card_header("Sales by Country"),
        ui.output_ui("map_chart"),
        full_screen=True,
    )
