"""Dashboard tab panel: filters in sidebar, KPIs, map, leaderboard, revenue trend."""

from shiny import ui

# Relative imports when used as package (e.g. from app)
try:
    from .filters import filters_sidebar_ui
    from .value_boxes import value_boxes_ui
    from .map_chart import map_chart_ui
    from .leaderboard import leaderboard_ui
    from .revenue_trend import revenue_trend_ui
    from .product_revenue import product_revenue_ui
    from .footer import footer_ui
except ImportError:
    from filters import filters_sidebar_ui
    from value_boxes import value_boxes_ui
    from map_chart import map_chart_ui
    from leaderboard import leaderboard_ui
    from revenue_trend import revenue_trend_ui
    from product_revenue import product_revenue_ui
    from footer import footer_ui


def dashboard_panel_ui(
    countries: list,
    products: list,
    date_start: str,
    date_end: str,
    years: list[int],
    date_default_start: str | None = None,
):
    """Build the Chocolate Sales Dashboard tab panel content (filters in left sidebar)."""
    if date_default_start is None:
        date_default_start = date_start
    sidebar = ui.sidebar(
        filters_sidebar_ui(
            countries, products, date_start, date_end, years, date_default_start
        ),
        title="Filters",
        position="left",
        open="open",
    )
    main_content = ui.tags.div(
        ui.layout_columns(
            ui.tags.div(value_boxes_ui()),
            ui.tags.div(product_revenue_ui()),
            col_widths=(8, 4),
        ),
        ui.layout_columns(
            ui.tags.div(map_chart_ui()),
            ui.tags.div(revenue_trend_ui()),
            col_widths=(6, 6),
        ),
        ui.tags.div(leaderboard_ui()),
        footer_ui()
    )
    return ui.layout_sidebar(
        sidebar,
        main_content,
        fillable=True,
        fill=True,
    )
