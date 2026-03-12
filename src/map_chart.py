"""World choropleth map: revenue by country."""

import pandas as pd
import altair as alt
from shiny import ui

# JS injected into the map iframe to forward country clicks to the parent Shiny app
_MAP_CLICK_JS = """\
  <script>
    (function() {
      var _orig = window.vegaEmbed;
      window.vegaEmbed = function(el, spec, opt) {
        return _orig(el, spec, opt).then(function(result) {
          result.view.addEventListener('click', function(event, item) {
            if (item && item.datum && item.datum['Country']) {
              window.parent.postMessage(
                {type: 'cocoa_map_click', country: item.datum['Country']}, '*'
              );
            }
          });
          return result;
        });
      };
    })();
  </script>
"""

_IIFE_MARKER = "  <script>\n    (function(vegaEmbed) {"


def _inject_click_handler(html: str) -> str:
    """Patch vegaEmbed in chart HTML to send clicked country name to parent via postMessage."""
    return html.replace(_IIFE_MARKER, _MAP_CLICK_JS + _IIFE_MARKER, 1)


def map_chart_ui():
    """Build the world map card."""
    return ui.card(
        ui.card_header("Sales by Country (click to filter)"),
        ui.output_ui("map_chart"),
        full_screen=True,
        class_="card-bg-white",
    )


def country_choropleth_ui(
    data: pd.DataFrame,
    country_codes: dict,
    world_topo_url: str,
    chart_height: int = 320,
    iframe_height: str = "350px",
    clickable: bool = False,
    selected_countries: list | None = None,
):
    """
    Build a country revenue choropleth UI from transaction data.
    Returns ui.p if no data, else an iframe with the chart.
    """
    if data is None or data.empty:
        return ui.p("No data to display.")

    country_sales = (
        data.groupby("Country")["Amount"].sum().reset_index()
    )
    country_sales["id"] = country_sales["Country"].map(country_codes)

    topo = alt.topo_feature(world_topo_url, "countries")
    background = (
        alt.Chart(topo)
        .mark_geoshape(fill="#8C8C8C", stroke="white", strokeWidth=0.5)
        .project("naturalEarth1")
        .properties(width="container", height=chart_height)
    )
    max_amount = float(country_sales["Amount"].max())
    fixed_color = alt.Color(
        "Amount:Q",
        scale=alt.Scale(scheme="oranges", domain=[0, max_amount]),
        legend=alt.Legend(
            title="Revenue (USD)",
            labelExpr="'$' + format(datum.value / 1000, ',.0f') + 'K'",
        ),
    )
    sales_layer = (
        alt.Chart(topo)
        .mark_geoshape(stroke="white", strokeWidth=0.5)
        .encode(
            color=fixed_color,
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
        .properties(width="container", height=chart_height)
    )
    if selected_countries:
        selected_sales = country_sales[country_sales["Country"].isin(selected_countries)]

        # All data countries in dark grey (unselected state)
        dimmed_layer = (
            alt.Chart(topo)
            .mark_geoshape(fill="#8C8C8C", stroke="white", strokeWidth=0.5)
            .transform_lookup(
                lookup="id",
                from_=alt.LookupData(country_sales, "id", ["Amount", "Country"]),
            )
            .project("naturalEarth1")
            .properties(width="container", height=chart_height)
        )
        # Only selected countries in orange on top, using the same fixed scale
        selected_layer = (
            alt.Chart(topo)
            .mark_geoshape(stroke="white", strokeWidth=0.5)
            .encode(
                color=fixed_color,
                tooltip=[
                    alt.Tooltip("Country:N", title="Country"),
                    alt.Tooltip("Amount:Q", format="$,.0f", title="Revenue"),
                ],
            )
            .transform_lookup(
                lookup="id",
                from_=alt.LookupData(selected_sales, "id", ["Amount", "Country"]),
            )
            .project("naturalEarth1")
            .properties(width="container", height=chart_height)
        )
        layers = [background, dimmed_layer, selected_layer]
    else:
        layers = [background, sales_layer]

    chart = alt.layer(*layers).configure_view(strokeWidth=0)
    html = chart.to_html()
    if clickable:
        html = _inject_click_handler(html)
    return ui.tags.iframe(
        srcdoc=html,
        style=f"width:100%;height:{iframe_height};border:none;",
    )
