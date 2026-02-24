from shiny import App, ui, render
import pandas as pd

from theme import get_head_content
from filters import filters_ui
from value_boxes import value_boxes_ui

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

app = App(app_ui, server)
