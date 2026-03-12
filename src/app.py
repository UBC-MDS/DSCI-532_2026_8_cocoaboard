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
    from .product_revenue import product_revenue_chart_ui
    from .kpi_calculations import (
        compute_yoy_badges_data,
        compute_mom_badges_data,
    )
else:
    from theme import get_head_content
    from constants import COUNTRY_CODES, WORLD_TOPO_URL
    from dashboard import dashboard_panel_ui
    from query_chat import create_query_chat, ai_chat_panel_ui
    from leaderboard import leaderboard_table_data
    from revenue_trend import revenue_trend_chart_ui
    from map_chart import country_choropleth_ui
    from product_revenue import product_revenue_chart_ui
    from kpi_calculations import (
        compute_yoy_badges_data,
        compute_mom_badges_data,
    )

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

# Available years for Year selector
years = sorted(
    t.mutate(year=t["Date"].year())
    .select("year")
    .distinct()
    .to_pandas()["year"]
    .astype(int)
    .tolist()
)

# Per-year date bounds (to set date range when a year is selected)
_year_bounds = (
    t.mutate(year=t["Date"].year())
    .group_by("year")
    .aggregate(year_start=t["Date"].min(), year_end=t["Date"].max())
    .to_pandas()
)
year_bounds = {
    str(int(r["year"])): (str(r["year_start"].date()), str(r["year_end"].date()))
    for _, r in _year_bounds.iterrows()
}
default_year = str(int(_dates["date_max"].year))

# -- QueryChat (AI chat) ------------------------------------------------------
df = t.to_pandas() # convert the lazy ibis table expression to a dataFrame
qc = create_query_chat(df, api_key=os.environ.get("ANTHROPIC_API_KEY"))

# -- UI -----------------------------------------------------------------------
app_ui = ui.page_navbar(
    ui.nav_panel(
        "Chocolate Sales Dashboard",
        dashboard_panel_ui(countries, products, date_min, date_max, years, date_default_start),
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
    @reactive.effect
    @reactive.event(input.year)
    def _on_year_change():
        yr = input.year()
        if not yr:
            return
        if yr == "All":
            ui.update_date_range("date_range", start=date_min, end=date_max)
            return
        bounds = year_bounds.get(str(yr))
        if not bounds:
            return
        start, end = bounds
        ui.update_date_range("date_range", start=start, end=end)

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
            query = query.filter(t["Product"].isin(input.product()))
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
    def avg_revenue():
        data = filtered_data()
        if data.empty:
            return "$0"
        return f"${data['Amount'].mean():,.0f}"

    @render.ui
    def top_product_share():
        data = filtered_data()
        if data.empty:
            return ui.tags.div(
                ui.tags.div("No data", class_="kpi-subtitle"),
                ui.tags.div("N/A", class_="kpi-main"),
                class_="kpi-two-line",
            )
        by_product = data.groupby("Product")["Amount"].sum()
        total = by_product.sum()
        if total <= 0:
            return ui.tags.div(
                ui.tags.div("No data", class_="kpi-subtitle"),
                ui.tags.div("N/A", class_="kpi-main"),
                class_="kpi-two-line",
            )
        top_product = by_product.idxmax()
        share = by_product.max() / total * 100
        return ui.tags.div(
            ui.tags.div(str(top_product), class_="kpi-subtitle"),
            ui.tags.div(f"{share:,.1f}%", class_="kpi-main"),
            class_="kpi-two-line",
        )

    @render.ui
    def top_country_share():
        data = filtered_data()
        if data.empty:
            return ui.tags.div(
                ui.tags.div("No data", class_="kpi-subtitle"),
                ui.tags.div("N/A", class_="kpi-main"),
                class_="kpi-two-line",
            )
        by_country = data.groupby("Country")["Amount"].sum()
        total = by_country.sum()
        if total <= 0:
            return ui.tags.div(
                ui.tags.div("No data", class_="kpi-subtitle"),
                ui.tags.div("N/A", class_="kpi-main"),
                class_="kpi-two-line",
            )
        top_country = by_country.idxmax()
        share = by_country.max() / total * 100
        return ui.tags.div(
            ui.tags.div(str(top_country), class_="kpi-subtitle"),
            ui.tags.div(f"{share:,.1f}%", class_="kpi-main"),
            class_="kpi-two-line",
        )

    @reactive.calc
    def non_date_filtered_data():
        """Apply country and product filters but not date filter."""
        query = t
        if input.country():
            query = query.filter(t["Country"].isin(input.country()))
        if input.product():
            query = query.filter(t["Product"].isin(input.product()))
        return query.to_pandas()

    @render.ui
    def yoy_revenue():
        data = non_date_filtered_data()
        if data.empty:
            return ui.tags.div(
                ui.tags.div("No data", class_="kpi-subtitle"),
                ui.tags.div("N/A", class_="kpi-main"),
                class_="kpi-two-line",
            )

        badge_data = compute_yoy_badges_data(data, max_years=3)
        if not badge_data:
            return ui.tags.div(
                ui.tags.div("No data", class_="kpi-subtitle"),
                ui.tags.div("N/A", class_="kpi-main"),
                class_="kpi-two-line",
            )

        yoy_badges = []

        for entry in badge_data:
            year = entry["year"]
            pct = entry["pct"]
            direction = entry["direction"]

            if pct is None or direction == "neutral":
                badge = ui.tags.span(
                    f"{year} N/A", class_="kpi-badge kpi-badge-neutral"
                )
            else:
                arrow = "+" if pct >= 0 else "-"
                pct_abs = abs(pct)
                cls = (
                    "kpi-badge kpi-badge-positive"
                    if direction == "positive"
                    else "kpi-badge kpi-badge-negative"
                )
                badge = ui.tags.span(
                    f"{year} {arrow}{pct_abs:.1f}%", class_=cls
                )

            yoy_badges.append(badge)

        if not yoy_badges:
            return ui.tags.div(
                ui.tags.div("No data", class_="kpi-subtitle"),
                ui.tags.div("N/A", class_="kpi-main"),
                class_="kpi-two-line",
            )

        return ui.tags.div(
            ui.tags.div(
                "Last 3 years vs prior year", class_="kpi-subtitle"
            ),
            ui.tags.div(*yoy_badges, class_="kpi-badges"),
            class_="kpi-two-line",
        )

    @render.ui
    def mom_revenue():
        data = non_date_filtered_data()
        if data.empty:
            return ui.tags.div(
                ui.tags.div("No data", class_="kpi-subtitle"),
                ui.tags.div("N/A", class_="kpi-main"),
                class_="kpi-two-line",
            )

        badge_data = compute_mom_badges_data(data, max_months=3)
        if not badge_data:
            return ui.tags.div(
                ui.tags.div("No data", class_="kpi-subtitle"),
                ui.tags.div("N/A", class_="kpi-main"),
                class_="kpi-two-line",
            )

        mom_badges = []

        for entry in badge_data:
            label = entry["label"]
            pct = entry["pct"]
            direction = entry["direction"]

            if pct is None or direction == "neutral":
                badge = ui.tags.span(
                    f"{label} N/A",
                    class_="kpi-badge kpi-badge-neutral",
                )
            else:
                arrow = "+" if pct >= 0 else "-"
                pct_abs = abs(pct)
                cls = (
                    "kpi-badge kpi-badge-positive"
                    if direction == "positive"
                    else "kpi-badge kpi-badge-negative"
                )
                badge = ui.tags.span(
                    f"{label} {arrow}{pct_abs:.1f}%",
                    class_=cls,
                )

            mom_badges.append(badge)

        return ui.tags.div(
            ui.tags.div(
                "Last 3 months vs prior month", class_="kpi-subtitle"
            ),
            ui.tags.div(*mom_badges, class_="kpi-badges"),
            class_="kpi-two-line",
        )

    @render.ui
    def map_chart():
        selected = list(input.country()) if input.country() else None
        return country_choropleth_ui(
            map_data(), COUNTRY_CODES, WORLD_TOPO_URL, 340, "400px",
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

    @render.ui
    def product_revenue_chart():
        return product_revenue_chart_ui(filtered_data())

    @reactive.effect
    @reactive.event(input.clear_selections)
    def _clear_country_product():
        ui.update_selectize("country", selected=[])
        ui.update_selectize("product", selected=[])

    @reactive.effect
    @reactive.event(input.reset_filters)
    def _reset_all_filters():
        ui.update_date_range("date_range", start=date_default_start, end=date_max)
        ui.update_radio_buttons("year", selected=default_year)
        ui.update_selectize("country", selected=[])
        ui.update_selectize("product", selected=[])

    @reactive.effect
    @reactive.event(input.year)
    def _sync_date_range_to_year():
        selected = input.year()
        if not selected or selected == "All":
            return

        y = int(selected)
        # Clamp to dataset bounds when selecting boundary years
        start = f"{y}-01-01"
        end = f"{y}-12-31"
        if y == int(date_min[:4]):
            start = date_min
        if y == int(date_max[:4]):
            end = date_max
        ui.update_date_range("date_range", start=start, end=end)

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
