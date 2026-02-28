from shiny import App, ui, render, reactive
import pandas as pd
import altair as alt

from theme import get_head_content
from filters import filters_ui
from value_boxes import value_boxes_ui
from map_chart import map_chart_ui
from leaderboard import leaderboard_ui

# -- Constants ----------------------------------------------------------------
_COUNTRY_CODES = {
    "Australia": 36,
    "Canada": 124,
    "India": 356,
    "New Zealand": 554,
    "UK": 826,
    "USA": 840,
}
_WORLD_TOPO_URL = (
    "https://cdn.jsdelivr.net/npm/vega-datasets@v1.29.0/data/world-110m.json"
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
    ui.layout_columns(
        map_chart_ui(),
        leaderboard_ui(),
        col_widths=(7, 5),
    ),
)


# -- Server --------------------------------------------------------------------
def server(input, output, session):
    @reactive.calc
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
        return f"${filtered_data()['Amount'].sum():,.0f}"

    @render.text
    def total_boxes():
        return f"{filtered_data()['Boxes Shipped'].sum():,}"

    @render.text
    def active_reps():
        return str(filtered_data()["Sales Person"].nunique())

    @render.ui
    def map_chart():
        data = filtered_data()
        country_sales = (
            data.groupby("Country")["Amount"]
            .sum()
            .reset_index()
        )
        country_sales["id"] = country_sales["Country"].map(_COUNTRY_CODES)

        topo = alt.topo_feature(_WORLD_TOPO_URL, "countries")

        background = (
            alt.Chart(topo)
            .mark_geoshape(fill="#d3c4b4", stroke="white", strokeWidth=0.5)
            .project("naturalEarth1")
            .properties(width="container", height=320)
        )

        sales_layer = (
            alt.Chart(topo)
            .mark_geoshape(stroke="white", strokeWidth=0.5)
            .encode(
                color=alt.Color(
                    "Amount:Q",
                    scale=alt.Scale(scheme="oranges"),
                    legend=alt.Legend(title="Revenue (USD)"),
                ),
                tooltip=[
                    alt.Tooltip("Country:N", title="Country"),
                    alt.Tooltip("Amount:Q", format="$,.0f", title="Revenue"),
                ],
            )
            .transform_lookup(
                lookup="id",
                from_=alt.LookupData(country_sales, "id", ["Amount", "Country"]),
            )
            .project("naturalEarth1")
            .properties(width="container", height=320)
        )

        chart = (background + sales_layer).configure_view(strokeWidth=0)

        return ui.tags.iframe(
            srcdoc=chart.to_html(),
            style="width:100%;height:350px;border:none;",
        )

    @render.data_frame
    def leaderboard_table():
        data = filtered_data()
        leaderboard = (
            data.groupby("Sales Person")
            .agg(
                Revenue=("Amount", "sum"),
                Transactions=("Amount", "count"),
                Boxes=("Boxes Shipped", "sum"),
            )
            .reset_index()
            .sort_values("Revenue", ascending=False)
            .reset_index(drop=True)
        )
        leaderboard.insert(0, "Rank", range(1, len(leaderboard) + 1))
        leaderboard["Revenue"] = leaderboard["Revenue"].apply(lambda x: f"${x:,.0f}")
        leaderboard["Boxes"] = leaderboard["Boxes"].apply(lambda x: f"{x:,}")
        return leaderboard.rename(columns={"Sales Person": "Sales Rep"})


app = App(app_ui, server)
