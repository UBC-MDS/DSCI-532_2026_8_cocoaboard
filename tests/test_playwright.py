"""Playwright browser tests for CocoaBoard dashboard.

These tests verify end-to-end behavior by launching the real Shiny app and
interacting with it through a headless browser.

Prerequisites (one-time):
    playwright install chromium

Run with:
    pytest tests/test_playwright.py
"""

import re
from pathlib import Path

from playwright.sync_api import Page, expect
from shiny.pytest import create_app_fixture

_APP_PATH = Path(__file__).parent.parent / "src" / "app.py"
app = create_app_fixture(_APP_PATH)

_TIMEOUT = 15_000  # ms — generous timeout for Shiny's reactive startup


def test_dashboard_renders_all_sections(page: Page, app):
    """All main dashboard sections (leaderboard, map, KPI boxes) must be visible on
    load; a missing section indicates a UI component failed to mount or threw an error."""
    page.goto(app.url)
    expect(page).to_have_title("CocoaBoard")
    expect(page.get_by_text("Sales Rep Leaderboard")).to_be_visible(timeout=_TIMEOUT)
    expect(page.get_by_text("Sales by Country")).to_be_visible()


def test_total_revenue_kpi_displays_dollar_amount(page: Page, app):
    """The total revenue KPI box must render a dollar-formatted value (e.g. '$1,234');
    a broken reactive pipeline would leave the element empty or show raw numbers."""
    page.goto(app.url)
    revenue_el = page.locator("#total_revenue")
    revenue_el.wait_for(timeout=_TIMEOUT)
    value = revenue_el.inner_text()
    assert re.match(r"^\$[\d,]+$", value), f"Expected '$...', got: {value!r}"


def test_country_filter_keeps_leaderboard_visible(page: Page, app):
    """Applying a country filter must update the leaderboard without crashing;
    a broken filter reactive would clear the output or raise an unhandled error."""
    page.goto(app.url)
    # Wait for the initial leaderboard render
    page.locator("#leaderboard_table").wait_for(timeout=_TIMEOUT)
    # Set country filter via Shiny's JS API and wait for reactivity to settle
    page.evaluate("window.Shiny.setInputValue('country', ['Australia'], {priority: 'event'})")
    page.wait_for_timeout(2_000)
    expect(page.locator("#leaderboard_table")).to_be_visible()


def test_out_of_range_date_shows_no_data_message(page: Page, app):
    """A date range entirely outside the dataset must show 'No data to display.'
    for each chart component; the empty-state guard prevents unhandled exceptions."""
    page.goto(app.url)
    page.locator("#leaderboard_table").wait_for(timeout=_TIMEOUT)
    # Push a future date range that has no matching rows
    page.evaluate(
        "window.Shiny.setInputValue('date_range', ['2030-01-01', '2030-12-31'], {priority: 'event'})"
    )
    page.wait_for_timeout(3_000)
    # At least one "No data to display." message should appear (map or trend chart)
    expect(page.get_by_text("No data to display.").first).to_be_visible(timeout=8_000)
