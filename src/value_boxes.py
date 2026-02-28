"""KPI value boxes: Total Revenue, Total Boxes Shipped, Active Sales Reps."""

from shiny import ui

_ICON_COLOR = "#5D3A1A"
_ICON_SIZE = "2.5rem"

icon_revenue = ui.HTML(
    f'<i class="bi bi-currency-dollar" style="font-size: {_ICON_SIZE}; color: {_ICON_COLOR};"></i>'
)
icon_boxes = ui.HTML(
    f'<i class="bi bi-box-seam" style="font-size: {_ICON_SIZE}; color: {_ICON_COLOR};"></i>'
)
icon_reps = ui.HTML(
    f'<i class="bi bi-people" style="font-size: {_ICON_SIZE}; color: {_ICON_COLOR};"></i>'
)


def value_boxes_ui():
    """Build the row of KPI value boxes."""
    return ui.layout_columns(
        ui.value_box(
            "Total Revenue",
            ui.output_text("total_revenue"),
            showcase=icon_revenue,
            height="auto",
        ),
        ui.value_box(
            "Total Boxes Shipped",
            ui.output_text("total_boxes"),
            showcase=icon_boxes,
            height="auto",
        ),
        ui.value_box(
            "Active Sales Reps",
            ui.output_text("active_reps"),
            showcase=icon_reps,
            height="auto",
        ),
        col_widths=(4, 4, 4),
        fill=False,
        fillable=False,
    )
