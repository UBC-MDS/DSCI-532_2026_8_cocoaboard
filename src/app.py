"""CocoaBoard - Chocolate Sales Dashboard
Tab 1 — Dashboard: filters, KPIs, choropleth map, leaderboard.
Tab 2 — AI Chat: querychat natural-language filtering & visualizations
"""

from shiny import App, ui, render, reactive
import pandas as pd
import altair as alt
from pathlib import Path
import sys

import querychat
from chatlas import ChatAnthropic
from dotenv import load_dotenv

# Load environment variables (.env for local dev; env vars on Connect Cloud)
load_dotenv()

# When run as a script (e.g. shiny run src/app.py), __package__ is unset;
# add src to path so absolute imports work. When run as src.app (e.g. on
# Connect), __package__ is "src" and we use relative imports.
if not __package__ or __package__ == "__main__":
    _src = Path(__file__).resolve().parent
    if str(_src) not in sys.path:
        sys.path.insert(0, str(_src))

if __package__ and __package__ != "__main__":
    from .theme import get_head_content
    from .filters import filters_ui
    from .value_boxes import value_boxes_ui
    from .map_chart import map_chart_ui
    from .leaderboard import leaderboard_ui
else:
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

# -- querychat setup ----------------------------------------------------------
qc = querychat.QueryChat(
    df.copy(),
    "chocolate_sales",
    greeting="""Ask me anything about CocoaBoard chocolate sales data.

* <span class="suggestion">Show sales from Australia</span>
* <span class="suggestion">Which sales rep has the highest revenue?</span>
* <span class="suggestion">Filter to Mint Chip Choco products</span>
* <span class="suggestion">Show top 10 transactions by amount</span>
""",
    data_description="""
Chocolate sales transaction data with the following columns:
- Sales Person: name of the sales representative
- Country: one of Australia, Canada, India, New Zealand, UK, USA
- Product: chocolate product name (e.g. Mint Chip Choco, 85% Dark Bars, Peanut Butter Cubes)
- Date: transaction date (datetime)
- Amount: sale amount in USD (float)
- Boxes Shipped: number of boxes shipped (integer)
""",
    client=ChatAnthropic(model="claude-haiku-4-5"),
)

# -- Footer -------------------------------------------------------------------
_footer = ui.tags.footer(
    "CocoaBoard | Created by Daisy Zhou, Vinay Valson, Eduardo Rivera | ",
    ui.tags.a(
        "GitHub Repo",
        href="https://github.com/UBC-MDS/DSCI-532_2026_8_cocoaboard",
        target="_blank",
    ),
    " | Last updated: March 2026",
    style=(
        "text-align: center; padding: 1rem; margin-top: 2rem; "
        "font-size: 0.85rem; color: #666; border-top: 1px solid #C4A35A;"
    ),
)

# -- UI -----------------------------------------------------------------------
app_ui = ui.page_navbar(
    # ── Tab 1: Traditional Dashboard ─────────────────────────────────────────
    ui.nav_panel(
        "Chocolate Sales Dashboard",
        ui.tags.div(
            filters_ui(countries, products, "2024-08-01", "2024-08-31"), #set the default date range to 2025
            value_boxes_ui(),
            ui.layout_columns(
                ui.card(
                    map_chart_ui(),
                    style="height: 450px; overflow-y: auto;",
                ),
                ui.card(
                    leaderboard_ui(),
                    style="height: 450px; overflow-y: auto;",
                ),
                col_widths=(7, 5),
            ),
            _footer,
            style="padding: 1rem;",
        ),
    ),

    # ── Tab 2: AI Chat ────────────────────────────────────────────────────────
    ui.nav_panel(
        "AI Chat Helper",
        ui.layout_sidebar(
            qc.sidebar(),
            ui.tags.div(
                # Download button
                ui.card(
                    ui.download_button(
                        "download_ai_data",
                        "Download Filtered Data",
                        class_="btn-sm",
                    ),
                    style="padding: 0.5rem;",
                ),
                # Filtered dataframe
                ui.card(
                    ui.card_header(ui.output_text("ai_chat_title")),
                    ui.output_data_frame("ai_chat_table"),
                    full_screen=True,
                ),
                # Two visualizations
                ui.layout_columns(
                    ui.card(
                        ui.card_header("Revenue by Country"),
                        ui.output_ui("ai_map_chart"),
                        full_screen=True,
                    ),
                    ui.card(
                        ui.card_header("Top Sales Reps"),
                        ui.output_ui("ai_leaderboard_chart"),
                        full_screen=True,
                    ),
                    col_widths=(6, 6),
                ),
                style="padding: 1rem;",
            ),
            fillable=True,
        ),
    ),

    title="CocoaBoard",
    header=get_head_content(),
    fillable=True,
)

# -- Server --------------------------------------------------------------------
def server(input, output, session):
    # ── Tab 1: traditional dashboard ─────────────────────────────────────────
    @reactive.calc
    def filtered_data():
        data = df.copy()
        start, end = input.date_range()
        data = data[
            (data["Date"] >= pd.Timestamp(start)) & (data["Date"] <= pd.Timestamp(end))
        ]
        # multi-select: empty tuple/None means "All"
        if input.country():
            data = data[data["Country"].isin(input.country())]
        if input.product():
            data = data[data["Product"].isin(input.product())]
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
        total_revenue = data["Amount"].sum()
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
        leaderboard["Avg Deal"] = (leaderboard["Revenue"] / leaderboard["Transactions"]).apply(lambda x: f"${x:,.0f}")
        leaderboard["Rev Share"] = (leaderboard["Revenue"] / total_revenue * 100).apply(lambda x: f"{x:.1f}%")
        leaderboard["Revenue"] = leaderboard["Revenue"].apply(lambda x: f"${x:,.0f}")
        leaderboard["Boxes"] = leaderboard["Boxes"].apply(lambda x: f"{x:,}")
        leaderboard = leaderboard.rename(columns={"Sales Person": "Sales Rep"})

        # Summary row with means/totals
        summary = pd.DataFrame([{
            "Rank": "",
            "Sales Rep": "AVERAGE / TOTAL",
            "Revenue": f"${total_revenue:,.0f}",
            "Transactions": data.shape[0],
            "Boxes": f"{data['Boxes Shipped'].sum():,}",
            "Avg Deal": f"${data['Amount'].mean():,.0f}",
            "Rev Share": "100.0%",
        }])
        return pd.concat([leaderboard, summary], ignore_index=True)
    
    # ── Tab 2: AI chat ────────────────────────────────────────────────────────
    qc_vals = qc.server()

    @render.text
    def ai_chat_title():
        return qc_vals.title() or "Chocolate Sales Data"

    @render.data_frame
    def ai_chat_table():
        return qc_vals.df()

    @render.download(filename="filtered_chocolate_sales.csv")
    def download_ai_data():
        yield qc_vals.df().to_csv(index=False)

    @render.ui
    def ai_map_chart():
        data = qc_vals.df()
        if data is None or data.empty:
            return ui.p("No data to display.")
        country_sales = (
            data.groupby("Country")["Amount"].sum().reset_index()
        )
        country_sales["id"] = country_sales["Country"].map(_COUNTRY_CODES)
        topo = alt.topo_feature(_WORLD_TOPO_URL, "countries")
        background = (
            alt.Chart(topo)
            .mark_geoshape(fill="#d3c4b4", stroke="white", strokeWidth=0.5)
            .project("naturalEarth1")
            .properties(width="container", height=280)
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
            .properties(width="container", height=280)
        )
        chart = (background + sales_layer).configure_view(strokeWidth=0)
        return ui.tags.iframe(
            srcdoc=chart.to_html(),
            style="width:100%;height:310px;border:none;",
        )


app = App(app_ui, server)
