from shiny import App, ui, render
import pandas as pd

from theme import get_head_content
from filters import filters_ui
from value_boxes import value_boxes_ui
from revenue_chart import revenue_chart_ui, build_chart
from tables import (
    top_products_ui,
    top_countries_ui,
    leaderboard_ui,
    get_top_products_df,
    get_top_countries_df,
    get_leaderboard_df,
)

# -- Load data ----------------------------------------------------------------
df = pd.read_csv("data/raw/Chocolate_Sales.csv")
df["Amount"] = df["Amount"].str.replace(r"[\$,]", "", regex=True).astype(float)
df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")

countries = sorted(df["Country"].unique().tolist())
products = sorted(df["Product"].unique().tolist())
date_min = str(df["Date"].min().date())
date_max = str(df["Date"].max().date())

# -- UI -----------------------------------------------------------------------
app_ui = ui.page_fillable(
    get_head_content(),
    ui.h2("CocoaBoard - Chocolate Sales Dashboard"),
    filters_ui(countries, products, date_min, date_max),
    value_boxes_ui(),
    revenue_chart_ui(),
    ui.layout_columns(
        top_products_ui(),
        top_countries_ui(),
        col_widths=(6, 6),
        fill=False,
        fillable=False,
    ),
    ui.layout_columns(
        leaderboard_ui(),
        col_widths=(12,),
        fill=False,
        fillable=False,
    ),
)


# -- Server --------------------------------------------------------------------
def server(input, output, session):
    def filtered_data():
        data = df.copy()
        start, end = input.date_range()
        data = data[
            (data["Date"] >= pd.Timestamp(start)) & (data["Date"] <= pd.Timestamp(end))
        ]
        if input.country() != "All":
            data = data[data["Country"] == input.country()]
        if input.product() != "All":
            data = data[data["Product"] == input.product()]
        return data

    @render.text
    def total_revenue():
        data = filtered_data()
        return f"${data['Amount'].sum():,.0f}"

    @render.text
    def total_boxes():
        data = filtered_data()
        return f"{data['Boxes Shipped'].sum():,}"

    @render.text
    def active_reps():
        data = filtered_data()
        return str(data["Sales Person"].nunique())

    @render.ui
    def revenue_chart():
        data = filtered_data()
        monthly = (
            data.assign(Month=data["Date"].dt.to_period("M").dt.to_timestamp())
            .groupby("Month")["Amount"]
            .sum()
            .reset_index()
        )
        return build_chart(monthly)

    @render.table
    def top_products():
        return get_top_products_df(filtered_data())

    @render.table
    def top_countries():
        return get_top_countries_df(filtered_data())

    @render.table
    def leaderboard():
        return get_leaderboard_df(filtered_data())


app = App(app_ui, server)
