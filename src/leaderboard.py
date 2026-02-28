"""Salesperson leaderboard table."""

from shiny import ui


def leaderboard_ui():
    """Build the salesperson leaderboard card."""
    return ui.card(
        ui.card_header("Sales Rep Leaderboard"),
        ui.output_data_frame("leaderboard_table"),
        full_screen=True,
    )
