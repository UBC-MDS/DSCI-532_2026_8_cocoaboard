"""Table widgets: Top 5 Products, Top 5 Countries, Salesperson Leaderboard."""

import pandas as pd
from shiny import ui


def top_products_ui():
    """Build the Top 5 Products card UI."""
    return ui.card(
        ui.card_header("Top 5 Products"),
        ui.output_table("top_products"),
    )


def top_countries_ui():
    """Build the Top 5 Countries card UI."""
    return ui.card(
        ui.card_header("Top 5 Countries"),
        ui.output_table("top_countries"),
    )


def leaderboard_ui():
    """Build the Salesperson Performance Leaderboard card UI."""
    return ui.card(
        ui.card_header("Salesperson Performance Leaderboard"),
        ui.output_table("leaderboard"),
    )


def get_top_products_df(data: pd.DataFrame) -> pd.DataFrame:
    """Aggregate and return top 5 products by revenue."""
    return (
        data.groupby("Product")
        .agg(Revenue=("Amount", "sum"), Transactions=("Amount", "count"))
        .sort_values("Revenue", ascending=False)
        .head(5)
        .reset_index()
    )


def get_top_countries_df(data: pd.DataFrame) -> pd.DataFrame:
    """Aggregate and return top 5 countries by revenue."""
    return (
        data.groupby("Country")
        .agg(Revenue=("Amount", "sum"), Transactions=("Amount", "count"))
        .sort_values("Revenue", ascending=False)
        .head(5)
        .reset_index()
    )


def get_leaderboard_df(data: pd.DataFrame) -> pd.DataFrame:
    """Aggregate and return salesperson leaderboard with rank."""
    return (
        data.groupby("Sales Person")
        .agg(Revenue=("Amount", "sum"), Transactions=("Amount", "count"))
        .sort_values("Revenue", ascending=False)
        .reset_index()
        .rename(columns={"Sales Person": "Salesperson"})
        .assign(Rank=lambda x: range(1, len(x) + 1))[
            ["Rank", "Salesperson", "Revenue", "Transactions"]
        ]
    )
