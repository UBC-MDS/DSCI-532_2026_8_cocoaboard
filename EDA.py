import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

# Configuration for Plotly
pio.renderers.default = "png"

COLORS = [
    "#6B3A2A", "#8B5E3C", "#A0522D", "#C68E6E", "#D2A679",
    "#E6C9A8", "#F5DEB3", "#DEB887", "#D2B48C", "#BC8F6F",
    "#A47551", "#7B4B3A", "#4E3226", "#C4A77D", "#B8860B",
    "#DAA06D", "#E8CEAB", "#F0E0C8", "#C19A6B", "#A67B5B",
    "#8C6545", "#6F4E37", "#5C3D2E", "#D4A76A", "#BFA07A",
]

# Load data
df = pd.read_csv("data/raw/Chocolate_Sales.csv")

# Clean Amount column: remove $ and commas, convert to float
df["Amount"] = df["Amount"].str.replace("$", "", regex=False).str.replace(",", "", regex=False).astype(float)

# Parse Date column
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
df["Month"] = df["Date"].dt.to_period("M").astype(str)

print("Data Head:")
print(df.head())

# Data Info and Describe
print("
Data Info:")
df.info()
print("
Data Description:")
print(df.describe())

# Distribution of Sales Amount
fig1 = go.Figure(go.Histogram(x=df["Amount"], nbinsx=30, marker_color=COLORS[0]))
fig1.update_layout(title="Distribution of Sales Amount", xaxis_title="Amount", yaxis_title="Count")
fig1.show()

# Total Sales by Country
sales_by_country = df.groupby("Country", as_index=False)["Amount"].sum().sort_values("Amount", ascending=False)
fig2 = go.Figure(go.Bar(
    x=sales_by_country["Country"],
    y=sales_by_country["Amount"],
    marker_color=COLORS[:len(sales_by_country)],
))
fig2.update_layout(title="Total Sales by Country", xaxis_title="Country", yaxis_title="Amount")
fig2.show()

# Total Sales by Product
sales_by_product = df.groupby("Product", as_index=False)["Amount"].sum().sort_values("Amount")
fig3 = go.Figure(go.Bar(
    x=sales_by_product["Amount"],
    y=sales_by_product["Product"],
    orientation="h",
    marker_color=COLORS[:len(sales_by_product)],
))
fig3.update_layout(title="Total Sales by Product", xaxis_title="Amount", yaxis_title="Product")
fig3.show()

# Monthly Sales Trend
monthly_sales = df.groupby("Month", as_index=False)["Amount"].sum()
fig4 = go.Figure(go.Scatter(
    x=monthly_sales["Month"],
    y=monthly_sales["Amount"],
    mode="lines+markers",
    line_color=COLORS[0],
    marker_color=COLORS[2],
))
fig4.update_layout(title="Monthly Sales Trend", xaxis_title="Month", yaxis_title="Amount")
fig4.show()

# Top 10 Sales People by Total Sales
top_sellers = df.groupby("Sales Person", as_index=False)["Amount"].sum().sort_values("Amount").tail(10)
fig5 = go.Figure(go.Bar(
    x=top_sellers["Amount"],
    y=top_sellers["Sales Person"],
    orientation="h",
    marker_color=COLORS[:len(top_sellers)],
))
fig5.update_layout(title="Top 10 Sales People by Total Sales", xaxis_title="Amount", yaxis_title="Sales Person")
fig5.show()

# Boxes Shipped vs Sales Amount (colored by Country)
fig6 = go.Figure()
for i, country in enumerate(df["Country"].unique()):
    subset = df[df["Country"] == country]
    fig6.add_trace(go.Scatter(
        x=subset["Boxes Shipped"],
        y=subset["Amount"],
        mode="markers",
        name=country,
        marker_color=COLORS[i % len(COLORS)],
    ))
fig6.update_layout(title="Boxes Shipped vs Sales Amount", xaxis_title="Boxes Shipped", yaxis_title="Amount")
fig6.show()

# Sales Amount Distribution by Country
fig7 = go.Figure()
for i, country in enumerate(df["Country"].unique()):
    subset = df[df["Country"] == country]
    fig7.add_trace(go.Box(
        y=subset["Amount"],
        name=country,
        marker_color=COLORS[i % len(COLORS)],
    ))
fig7.update_layout(title="Sales Amount Distribution by Country", yaxis_title="Amount")
fig7.show()

# Monthly Sales Trend by Country
monthly_country = df.groupby(["Month", "Country"], as_index=False)["Amount"].sum()
fig8 = go.Figure()
for i, country in enumerate(monthly_country["Country"].unique()):
    subset = monthly_country[monthly_country["Country"] == country]
    fig8.add_trace(go.Scatter(
        x=subset["Month"],
        y=subset["Amount"],
        mode="lines+markers",
        name=country,
        marker_color=COLORS[i % len(COLORS)],
    ))
fig8.update_layout(title="Monthly Sales Trend by Country", xaxis_title="Month", yaxis_title="Amount")
fig8.show()

# Monthly Sales by Product (Stacked Area)
product_monthly = df.groupby(["Month", "Product"], as_index=False)["Amount"].sum()
fig9 = go.Figure()
for i, product in enumerate(product_monthly["Product"].unique()):
    subset = product_monthly[product_monthly["Product"] == product]
    fig9.add_trace(go.Scatter(
        x=subset["Month"],
        y=subset["Amount"],
        mode="lines",
        name=product,
        stackgroup="one",
        line_color=COLORS[i % len(COLORS)],
    ))
fig9.update_layout(title="Monthly Sales by Product (Stacked Area)", xaxis_title="Month", yaxis_title="Amount")
fig9.show()
