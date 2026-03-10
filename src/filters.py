"""Filter widget: date range, country, product. Card layout or sidebar content."""

from shiny import ui


def _filter_inputs(
    countries: list[str],
    products: list[str],
    date_min: str,
    date_max: str,
    date_default_start: str,
):
    """Shared filter inputs (date, country, product). Used by both card and sidebar."""
    return [
        ui.input_date_range(
            "date_range",
            "Date Range",
            start=date_default_start,
            end=date_max,
            min=date_min,
            max=date_max,
        ),
        ui.input_selectize(
            "country",
            "Country",
            choices=countries,
            selected=None,
            multiple=True,
            options={"placeholder": "All countries"},
        ),
        ui.input_selectize(
            "product",
            "Product",
            choices=products,
            selected=None,
            multiple=True,
            options={"placeholder": "All products"},
        ),
    ]


def filters_ui(
    countries: list[str],
    products: list[str],
    date_min: str,
    date_max: str,
    date_default_start: str | None = None,
):
    """Build the filters card UI with filters arranged in a row (legacy/inline use)."""
    if date_default_start is None:
        date_default_start = date_min
    return ui.layout_columns(
        ui.card(
            ui.card_header("Filters"),
            ui.layout_columns(
                *_filter_inputs(countries, products, date_min, date_max, date_default_start),
                col_widths=(4, 4, 4),
                fill=False,
                fillable=False,
            ),
        ),
        col_widths=(12,),
        fill=False,
        fillable=False,
    )


def filters_sidebar_ui(
    countries: list[str],
    products: list[str],
    date_min: str,
    date_max: str,
    date_default_start: str | None = None,
):
    """Build filter inputs for use inside a collapsible sidebar (stacked vertically)."""
    if date_default_start is None:
        date_default_start = date_min
    return ui.tags.div(
        *_filter_inputs(countries, products, date_min, date_max, date_default_start),
        style="display: flex; flex-direction: column; gap: 1rem;",
    )
