"""Salesperson leaderboard table."""

import pandas as pd
from shiny import ui


def leaderboard_ui():
    """Build the salesperson leaderboard card."""
    return ui.card(
        ui.card_header("Sales Rep Leaderboard"),
        ui.output_data_frame("leaderboard_table"),
        full_screen=True,
    )


def leaderboard_table_data(data: pd.DataFrame) -> pd.DataFrame:
    """Build leaderboard DataFrame with rank, revenue, transactions, summary row."""
    if data.empty:
        return pd.DataFrame(
            columns=["Rank", "Sales Rep", "Revenue", "Transactions", "Boxes", "Avg Deal", "Rev Share"]
        )
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
    leaderboard["Avg Deal"] = (
        leaderboard["Revenue"] / leaderboard["Transactions"]
    ).apply(lambda x: f"${x:,.0f}")
    leaderboard["Rev Share"] = (
        leaderboard["Revenue"] / total_revenue * 100
    ).apply(lambda x: f"{x:.1f}%")
    leaderboard["Revenue"] = leaderboard["Revenue"].apply(lambda x: f"${x:,.0f}")
    leaderboard["Boxes"] = leaderboard["Boxes"].apply(lambda x: f"{x:,}")
    leaderboard = leaderboard.rename(columns={"Sales Person": "Sales Rep"})

    summary = pd.DataFrame(
        [
            {
                "Rank": "",
                "Sales Rep": "AVERAGE / TOTAL",
                "Revenue": f"${total_revenue:,.0f}",
                "Transactions": data.shape[0],
                "Boxes": f"{data['Boxes Shipped'].sum():,}",
                "Avg Deal": f"${data['Amount'].mean():,.0f}",
                "Rev Share": "100.0%",
            }
        ]
    )
    return pd.concat([leaderboard, summary], ignore_index=True)
