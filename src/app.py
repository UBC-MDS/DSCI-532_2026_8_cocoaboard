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
import ibis

load_dotenv()
ibis.options.interactive = True

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
    from .kpi_calculations import compute_yoy_revenue, compute_mom_revenue
else:
    from theme import get_head_content
    from constants import COUNTRY_CODES, WORLD_TOPO_URL
    from dashboard import dashboard_panel_ui
    from query_chat import create_query_chat, ai_chat_panel_ui
    from leaderboard import leaderboard_table_data
    from revenue_trend import revenue_trend_chart_ui
    from map_chart import country_choropleth_ui
    from kpi_calculations import compute_yoy_revenue, compute_mom_revenue

# -- Load data via DuckDB (lazy) -----------------------------------------------
con = ibis.duckdb.connect()
t = con.read_parquet("data/processed/chocolate_sales.parquet")

# Extract filter choices and date bounds (small one-time queries)
countries = sorted(t.select("Country").distinct().to_pandas()["Country"].tolist())
products = sorted(t.select("Product").distinct().to_pandas()["Product"].tolist())
_dates = t.select(
    date_min=t["Date"].min(),
    date_max=t["Date"].max(),
).to_pandas().iloc[0]
date_min = str(_dates["date_min"].date())
date_max = str(_dates["date_max"].date())
date_default_start = f"{_dates['date_max'].year}-01-01"

# -- QueryChat (AI chat) ------------------------------------------------------
df = t.to_pandas() # convert the lazy ibis table expression to a dataFrame
qc = create_query_chat(df, api_key=os.environ.get("ANTHROPIC_API_KEY"))

# -- UI -----------------------------------------------------------------------
app_ui = ui.page_navbar(
    ui.nav_panel(
        "Chocolate Sales Dashboard",
        dashboard_panel_ui(countries, products, date_min, date_max, date_default_start),
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
        query = t
        start, end = input.date_range()
        query = query.filter(
             (t["Date"] >= str(start)) & (t["Date"] <= str(end))
        )
        # multi-select: empty tuple/None means "All"
        if input.country():
            query = query.filter(t["Country"].isin(input.country()))
        if input.product():
            query = query.filter(t["Product"].isin(input.country()))
        return query.to_pandas()

    @reactive.calc
    def map_data():
        """Date- and product-filtered data for the map, without country filter.
        Keeps all countries visible and clickable regardless of the country selection.
        """
        query = t
        start, end = input.date_range()
        query = query.filter(
            (t["Date"] >= str(start)) & (t["Date"] <= str(end))
        )
        if input.product():
            query = query.filter(t["Product"].isin(input.product()))
        return query.to_pandas()

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
        query = t
        if input.country():
            query = query.filter(t["Country"].isin(input.country()))
        if input.product():
            query = query.filter(t["Product"].isin(input.product()))
        return query.to_pandas()

    @render.text
    def yoy_revenue():
        return compute_yoy_revenue(non_date_filtered_data())

    @render.text
    def mom_revenue():
        return compute_mom_revenue(non_date_filtered_data())

    @render.ui
    def map_chart():
        selected = list(input.country()) if input.country() else None
        return country_choropleth_ui(
            map_data(), COUNTRY_CODES, WORLD_TOPO_URL, 340, "370px",
            clickable=True, selected_countries=selected,
        )

    @reactive.effect
    def _on_map_country_click():
        country = input.map_clicked_country()
        if not country:
            return
        with reactive.isolate():
            current = list(input.country()) if input.country() else []
        if country in current:
            updated = [c for c in current if c != country]
        else:
            updated = current + [country]
        ui.update_selectize("country", selected=updated)

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
            qc_vals.df(), COUNTRY_CODES, WORLD_TOPO_URL, 280, "400px"
        )


app = App(app_ui, server)
