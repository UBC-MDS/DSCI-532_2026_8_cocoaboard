"""Dashboard tab panel: filters, KPIs, map, leaderboard, revenue trend."""

from shiny import ui

# Relative imports when used as package (e.g. from app)
try:
    from .filters import filters_ui
    from .value_boxes import value_boxes_ui
    from .map_chart import map_chart_ui
    from .leaderboard import leaderboard_ui
    from .revenue_trend import revenue_trend_ui
    from .footer import footer_ui
except ImportError:
    from filters import filters_ui
    from value_boxes import value_boxes_ui
    from map_chart import map_chart_ui
    from leaderboard import leaderboard_ui
    from revenue_trend import revenue_trend_ui
    from footer import footer_ui


def dashboard_panel_ui(
    countries: list,
    products: list,
    date_start: str,
    date_end: str,
    date_default_start: str | None = None,
):
    """Build the Chocolate Sales Dashboard tab panel content."""
    if date_default_start is None:
        date_default_start = date_start
    return ui.tags.div(
        filters_ui(countries, products, date_start, date_end, date_default_start),
        value_boxes_ui(),
        ui.layout_columns(
            ui.card(
                map_chart_ui(),
                style="height: 450px; overflow-y: auto;",
            ),
            ui.card(
                leaderboard_ui(),
                style="height: 450px; overflow-y: auto;",
            ),
            col_widths=(7, 5),
        ),
        ui.card(
            revenue_trend_ui(),
            style="height: 450px; overflow-y: auto;",
        ),
        footer_ui(),
        style="padding: 1rem;",
    )
