"""KPI value boxes: Total Revenue, Avg Revenue, YoY, MoM."""

from shiny import ui

_ICON_COLOR = "#5D3A1A"
_ICON_SIZE = "2.5rem"

icon_revenue = ui.HTML(
    f'<i class="bi bi-currency-dollar" style="font-size: {_ICON_SIZE}; color: {_ICON_COLOR};"></i>'
)
icon_avg = ui.HTML(
    f'<i class="bi bi-calculator" style="font-size: {_ICON_SIZE}; color: {_ICON_COLOR};"></i>'
)
icon_yoy = ui.HTML(
    f'<i class="bi bi-graph-up-arrow" style="font-size: {_ICON_SIZE}; color: {_ICON_COLOR};"></i>'
)
icon_mom = ui.HTML(
    f'<i class="bi bi-bar-chart-line" style="font-size: {_ICON_SIZE}; color: {_ICON_COLOR};"></i>'
)


def value_boxes_ui():
    """Build a 2x2 grid of KPI value boxes (4 cards)."""
    row1 = ui.layout_columns(
        ui.value_box(
            "Total Revenue",
            ui.output_text("total_revenue"),
            showcase=icon_revenue,
            height="auto",
        ),
        ui.value_box(
            "Avg Revenue (Filtered)",
            ui.output_text("avg_revenue"),
            showcase=icon_avg,
            height="auto",
        ),
        col_widths=(6, 6),
        fill=False,
        fillable=False,
    )
    row2 = ui.layout_columns(
        ui.value_box(
            "Year-over-Year Revenue",
            ui.output_text("yoy_revenue"),
            showcase=icon_yoy,
            height="auto",
        ),
        ui.value_box(
            "Month-over-Month Revenue",
            ui.output_text("mom_revenue"),
            showcase=icon_mom,
            height="auto",
        ),
        col_widths=(6, 6),
        fill=False,
        fillable=False,
    )
    return ui.tags.div(
        row1,
        row2,
        style="display: flex; flex-direction: column; gap: 0.75rem;",
    )
