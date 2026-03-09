"""CocoaBoard - Chocolate Sales Dashboard
Tab 1 — Dashboard: filters, KPIs, choropleth map, leaderboard.
Tab 2 — AI Chat: querychat natural-language filtering & visualizations
"""

from shiny import App, ui, render, reactive
import pandas as pd
from pathlib import Path
import sys
import os
from dotenv import load_dotenv

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
    from .constants import COUNTRY_CODES, WORLD_TOPO_URL
    from .dashboard import dashboard_panel_ui
    from .query_chat import create_query_chat, ai_chat_panel_ui
    from .leaderboard import leaderboard_table_data
    from .revenue_trend import revenue_trend_chart_ui
    from .map_chart import country_choropleth_ui
else:
    from theme import get_head_content
    from constants import COUNTRY_CODES, WORLD_TOPO_URL
    from dashboard import dashboard_panel_ui
    from query_chat import create_query_chat, ai_chat_panel_ui
    from leaderboard import leaderboard_table_data
    from revenue_trend import revenue_trend_chart_ui
    from map_chart import country_choropleth_ui

# -- Load data ----------------------------------------------------------------
df = pd.read_csv("data/raw/Chocolate_Sales.csv")
df["Amount"] = df["Amount"].str.replace(r"[\$,]", "", regex=True).astype(float)
df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")

countries = sorted(df["Country"].unique().tolist())
products = sorted(df["Product"].unique().tolist())

# -- QueryChat (AI chat) ------------------------------------------------------
qc = create_query_chat(df, api_key=os.environ.get("ANTHROPIC_API_KEY"))

# -- UI -----------------------------------------------------------------------
app_ui = ui.page_navbar(
    ui.nav_panel(
        "Chocolate Sales Dashboard",
        dashboard_panel_ui(countries, products, "2024-01-01", "2024-08-31"),
    ),
    ui.nav_panel(
        "AI Chat Helper",
        ai_chat_panel_ui(qc),
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

    @render.text
    def avg_revenue():
        data = filtered_data()
        if data.empty:
            return "$0"
        return f"${data['Amount'].mean():,.0f}"

    @reactive.calc
    def non_date_filtered_data():
        """Apply country and product filters but not date filter."""
        data = df.copy()
        if input.country():
            data = data[data["Country"].isin(input.country())]
        if input.product():
            data = data[data["Product"].isin(input.product())]
        return data

    @render.text
    def yoy_revenue():
        # Compare the last available year's revenue (up to its last month)
        # to the same months in the prior year. Responds to country/product filters.
        data = non_date_filtered_data()
        if data.empty:
            return "N/A"
        monthly = data.groupby(data["Date"].dt.to_period("M"))["Amount"].sum()
        last_date = data["Date"].max()
        current_year = last_date.year
        last_month = last_date.month
        current_rev = monthly[
            (monthly.index.year == current_year) & (monthly.index.month <= last_month)
        ].sum()
        prior_rev = monthly[
            (monthly.index.year == current_year - 1) & (monthly.index.month <= last_month)
        ].sum()
        if prior_rev == 0:
            return "N/A"
        pct = (current_rev - prior_rev) / prior_rev * 100
        arrow = "+" if pct >= 0 else ""
        return f"{arrow}{pct:.1f}%"

    @render.text
    def mom_revenue():
        # Compare the last available month's revenue to the prior month.
        # Responds to country/product filters.
        data = non_date_filtered_data()
        if data.empty:
            return "N/A"
        monthly = data.groupby(data["Date"].dt.to_period("M"))["Amount"].sum().sort_index()
        if len(monthly) < 2:
            return "N/A"
        current_rev = monthly.iloc[-1]
        prior_rev = monthly.iloc[-2]
        if prior_rev == 0:
            return "N/A"
        pct = (current_rev - prior_rev) / prior_rev * 100
        arrow = "+" if pct >= 0 else ""
        return f"{arrow}{pct:.1f}%"

    @render.ui
    def map_chart():
        return country_choropleth_ui(
            filtered_data(), COUNTRY_CODES, WORLD_TOPO_URL, 320, "350px"
        )

    @render.data_frame
    def leaderboard_table():
        return leaderboard_table_data(filtered_data())

    @render.ui
    def revenue_trend_chart():
        return revenue_trend_chart_ui(filtered_data())

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
        return country_choropleth_ui(
            qc_vals.df(), COUNTRY_CODES, WORLD_TOPO_URL, 280, "310px"
        )


app = App(app_ui, server)
