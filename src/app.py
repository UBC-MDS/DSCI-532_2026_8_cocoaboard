from shiny import App, ui, render
import pandas as pd
import altair as alt

# -- Load data ----------------------------------------------------------------
df = pd.read_csv("data/raw/Chocolate_Sales.csv")
df["Amount"] = df["Amount"].str.replace(r"[\$,]", "", regex=True).astype(float)
df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")

countries = sorted(df["Country"].unique().tolist())
products = sorted(df["Product"].unique().tolist())

# -- UI -----------------------------------------------------------------------
app_ui = ui.page_fillable(
    ui.h2("CocoaBoard – Chocolate Sales Dashboard"),

    # Filters row
    ui.layout_columns(
        ui.card(
            ui.card_header("Filters"),
            ui.input_date_range(
                "date_range", "Date Range",
                start=str(df["Date"].min().date()),
                end=str(df["Date"].max().date()),
            ),
            ui.input_selectize(
                "country", "Country",
                choices=["All"] + countries,
                selected="All",
            ),
            ui.input_selectize(
                "product", "Product",
                choices=["All"] + products,
                selected="All",
            ),
        ),
        col_widths=(12,),
    ),

    # KPI cards row
    ui.layout_columns(
        ui.value_box(
            "Total Revenue",
            ui.output_text("total_revenue"),
            showcase=ui.HTML("💰"),
        ),
        ui.value_box(
            "Total Boxes Shipped",
            ui.output_text("total_boxes"),
            showcase=ui.HTML("📦"),
        ),
        ui.value_box(
            "Active Sales Reps",
            ui.output_text("active_reps"),
            showcase=ui.HTML("👤"),
        ),
        col_widths=(4, 4, 4),
    ),

    # Revenue Over Time chart
    ui.layout_columns(
        ui.card(
            ui.card_header("Revenue Over Time"),
            ui.output_ui("revenue_chart"),
        ),
        col_widths=(12,),
    ),

    # Bottom row: Top Products, Top Countries, Salesperson Leaderboard
    ui.layout_columns(
        ui.card(
            ui.card_header("Top 5 Products"),
            ui.output_table("top_products"),
        ),
        ui.card(
            ui.card_header("Top 5 Countries"),
            ui.output_table("top_countries"),
        ),
        col_widths=(6, 6),
    ),

    ui.layout_columns(
        ui.card(
            ui.card_header("Salesperson Performance Leaderboard"),
            ui.output_table("leaderboard"),
        ),
        col_widths=(12,),
    ),
)


# -- Server --------------------------------------------------------------------
def server(input, output, session):

    def filtered_data():
        data = df.copy()
        start, end = input.date_range()
        data = data[(data["Date"] >= pd.Timestamp(start)) & (data["Date"] <= pd.Timestamp(end))]
        if input.country() != "All":
            data = data[data["Country"] == input.country()]
        if input.product() != "All":
            data = data[data["Product"] == input.product()]
        return data

    @render.text
    def total_revenue():
        data = filtered_data()
        return f"${data['Amount'].sum():,.0f}"

    @render.text
    def total_boxes():
        data = filtered_data()
        return f"{data['Boxes Shipped'].sum():,}"

    @render.text
    def active_reps():
        data = filtered_data()
        return str(data["Sales Person"].nunique())

    @render.ui
    def revenue_chart():
        data = filtered_data()
        monthly = (
            data.assign(Month=data["Date"].dt.to_period("M").dt.to_timestamp())
            .groupby("Month")["Amount"]
            .sum()
            .reset_index()
        )
        chart = (
            alt.Chart(monthly)
            .mark_line(point=True)
            .encode(
                x=alt.X("Month:T", title="Date"),
                y=alt.Y("Amount:Q", title="Revenue (USD)"),
                tooltip=["Month:T", "Amount:Q"],
            )
            .properties(width="container", height=300)
        )
        return ui.HTML(chart.to_html())

    @render.table
    def top_products():
        data = filtered_data()
        return (
            data.groupby("Product")
            .agg(Revenue=("Amount", "sum"), Transactions=("Amount", "count"))
            .sort_values("Revenue", ascending=False)
            .head(5)
            .reset_index()
        )

    @render.table
    def top_countries():
        data = filtered_data()
        return (
            data.groupby("Country")
            .agg(Revenue=("Amount", "sum"), Transactions=("Amount", "count"))
            .sort_values("Revenue", ascending=False)
            .head(5)
            .reset_index()
        )

    @render.table
    def leaderboard():
        data = filtered_data()
        return (
            data.groupby("Sales Person")
            .agg(Revenue=("Amount", "sum"), Transactions=("Amount", "count"))
            .sort_values("Revenue", ascending=False)
            .reset_index()
            .rename(columns={"Sales Person": "Salesperson"})
            .assign(Rank=lambda x: range(1, len(x) + 1))
            [["Rank", "Salesperson", "Revenue", "Transactions"]]
        )


app = App(app_ui, server)
