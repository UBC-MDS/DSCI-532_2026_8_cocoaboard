from shiny import App, ui

# -- UI -----------------------------------------------------------------------
app_ui = ui.page_fillable(
    ui.h2("CocoaBoard – Chocolate Sales Dashboard"),

    ui.layout_sidebar(
        ui.sidebar(
            ui.card_header("Filters"),
            "Date Range filter placeholder",
            "Country filter placeholder",
            "Product filter placeholder",
        ),

        # KPI cards row
        ui.layout_columns(
            ui.card(ui.card_header("Total Revenue")),
            ui.card(ui.card_header("Total Boxes Shipped")),
            ui.card(ui.card_header("Active Sales Reps")),
            col_widths=(4, 4, 4),
        ),

        # Revenue Over Time chart
        ui.layout_columns(
            ui.card(
                ui.card_header("Revenue Over Time"),
            ),
            col_widths=(12,),
        ),

        # Top Products & Top Countries
        ui.layout_columns(
            ui.card(ui.card_header("Top 5 Products")),
            ui.card(ui.card_header("Top 5 Countries")),
            col_widths=(6, 6),
        ),

        # Salesperson Leaderboard
        ui.layout_columns(
            ui.card(
                ui.card_header("Salesperson Performance Leaderboard"),
            ),
            col_widths=(12,),
        ),
    ),
)


def server(input, output, session):
    pass


app = App(app_ui, server)
