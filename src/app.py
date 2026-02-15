from shiny import App, ui

# -- UI -----------------------------------------------------------------------
app_ui = ui.page_fillable(
    ui.h2("CocoaBoard – Chocolate Sales Dashboard"),

    ui.layout_columns(
        ui.card(
            ui.card_header("Filters"),
        ),
        col_widths=(12,),
    ),

    ui.layout_columns(
        ui.card(ui.card_header("Total Revenue")),
        ui.card(ui.card_header("Total Boxes Shipped")),
        ui.card(ui.card_header("Active Sales Reps")),
        col_widths=(4, 4, 4),
    ),

    ui.layout_columns(
        ui.card(
            ui.card_header("Revenue Over Time"),
        ),
        col_widths=(12,),
    ),

    ui.layout_columns(
        ui.card(ui.card_header("Top 5 Products")),
        ui.card(ui.card_header("Top 5 Countries")),
        col_widths=(6, 6),
    ),

    ui.layout_columns(
        ui.card(
            ui.card_header("Salesperson Performance Leaderboard"),
        ),
        col_widths=(12,),
    ),
)


def server(input, output, session):
    pass


app = App(app_ui, server)
