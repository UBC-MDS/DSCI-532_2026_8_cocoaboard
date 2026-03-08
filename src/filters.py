"""Filter card widget: date range, country, product."""

from shiny import ui


def filters_ui(countries: list[str], products: list[str], date_min: str, date_max: str):
    """Build the filters card UI with filters arranged in a row."""
    return ui.layout_columns(
        ui.card(
            ui.card_header("Filters"),
            ui.layout_columns(
                ui.input_date_range(
                    "date_range",
                    "Date Range",
                    start=date_min,
                    end=date_max,
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
                col_widths=(4, 4, 4),
                fill=False,
                fillable=False,
            ),
        ),
        col_widths=(12,),
        fill=False,
        fillable=False,
    )
