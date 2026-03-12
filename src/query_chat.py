"""QueryChat (AI chat) setup and AI Chat Helper panel UI."""

import os
import querychat
from chatlas import ChatAnthropic
from shiny import ui


DATA_DESCRIPTION = """
Chocolate sales transaction data with the following columns:
- Sales Person: name of the sales representative (string)
- Country: one of Australia, Canada, India, New Zealand, UK, USA (string)
- Product: chocolate product name, e.g. Mint Chip Choco, 85% Dark Bars, Peanut Butter Cubes (string)
- Date: transaction date (datetime)
- Amount: sale amount in USD (float, e.g. 5320.00)
- Boxes Shipped: number of boxes shipped (integer)

IMPORTANT SQL CONSTRAINT: LIMIT is not supported. For "top N" queries, use a CTE
with ROW_NUMBER() window function and filter with WHERE rank <= N. Example:
  WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (ORDER BY Amount DESC) as rank
    FROM chocolate_sales
  )
  SELECT "Sales Person", Country, Product, Date, Amount, "Boxes Shipped"
  FROM ranked WHERE rank <= 10

Common queries: filter by country, product, sales person, date range,
or amount thresholds (e.g. Amount > 10000).
"""

CHAT_GREETING_DISABLED = (
    """**AI chat is disabled.** Set the `ANTHROPIC_API_KEY` environment variable to use this tab. """
    """Create a `.env` file in the project root with `ANTHROPIC_API_KEY=your_key_here` (see `.env.example`). """
    """Get a key at [Anthropic Console](https://console.anthropic.com/)."""
)

CHAT_GREETING_ENABLED = """Ask me anything about CocoaBoard chocolate sales data.

* <span class="suggestion">Show sales from Australia</span>
* <span class="suggestion">Which sales rep has the highest revenue?</span>
* <span class="suggestion">Filter to Mint Chip Choco products</span>
* <span class="suggestion">Show top 10 transactions by amount</span>
* <span class="suggestion">Show transactions over $10,000</span>
* <span class="suggestion">Compare revenue between UK and USA</span>
"""


def create_query_chat(df, api_key: str | None = None):
    """Create and return a QueryChat instance for the given dataframe."""
    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY") or ""
    greeting = CHAT_GREETING_DISABLED if not api_key else CHAT_GREETING_ENABLED
    qc = querychat.QueryChat(
        df.copy(),
        "chocolate_sales",
        greeting=greeting,
        data_description=DATA_DESCRIPTION,
        client=ChatAnthropic(model="claude-haiku-4-5", api_key=api_key),
    )
    return qc


def ai_chat_panel_ui(qc):
    """Build the AI Chat Helper tab panel content (sidebar + main area)."""
    return ui.layout_sidebar(
        qc.sidebar(),
        ui.tags.div(
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
            ui.card(
                ui.download_button(
                    "download_ai_data",
                    "Download Filtered Data",
                    class_="btn-sm",
                ),
                style="padding: 0.5rem;",
            ),
            ui.card(
                ui.card_header(ui.output_text("ai_chat_title")),
                ui.tags.div(
                    ui.output_data_frame("ai_chat_table"),
                    style=(
                        "min-height: 120px; max-height: 60vh; "
                        "overflow-y: auto; overflow-x: auto;"
                    ),
                ),
                full_screen=True,
            ),
            style="padding: 1rem;",
        ),
        fillable=True,
    )
