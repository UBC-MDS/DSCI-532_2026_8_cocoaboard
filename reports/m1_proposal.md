# Project Proposal for Chocolate Sales Dashboard

## Section 1: Motivation and Purpose

### Target Audience

Our target audience will be primarity Sales Managers, Regional Sales
Directors or C-suites at a chocolate manufacturing/distribution company.
Our team will serve as Data Analytics Consultants for the sales team
providing actionable insights to help the leadership team optimize their
sales strategy and resource allocation.

### Problem

Here are the challengs facing by the chocolate company:

-   Inconsistent sales performance across regions and salespeople: need
    to build performance tracker for sales strategy and human resource
    training
-   Inefficient product mix decisions: need to discover the top product
    sales for efficient recource allocation
-   Reactive rather than proactive management: Monthly or quarterly
    reviews happen too late to course-correct, and they need real-time
    visibility into trends
-   Missed opportunities: need to identify seasonal patterns, top
    customers, or which salesperson-product combinations work best

### Solution

Our interactive R Shiny dashboard will serve as a centralized, web-based
command center accessible from any browser. Through intuitive dropdown
filters, date selectors, and dynamic visualizations, sales managers can
instantly compare performance across salespeople, products, and
countries without technical expertise.

Interactive charts reveal trends over time, highlight top and
underperforming segments, and calculate profit margins on-the-fly. Users
can drill down from high-level overviews to granular transaction
details, answer ad-hoc questions independently, and even generate
personalized performance views for individual sales reps. This
self-service analytics tool transforms static data into actionable
intelligence, enabling the team to shift from reactive quarterly reviews
to proactive, data-driven decision-making in real-time.

## Section 2: Description of the Data

### Stats

The Chocolate Sales dataset contains 6 columns and provides
transactional-level sales data across multiple dimensions.

Columns: - Salesperson - The name of the salesperson responsible for the
sale. - Country - The country where the sale was made. - Product - The
name and type of the product sold. - Date - The date when the sale
transaction occurred (DD/MM/YYYY format). - Amount - The total sales
amount for the transaction, expressed in US dollars. - Boxes Shipped-
The number of product boxes shipped as part of the transaction.

### Relevance

Performance Tracking Variables: Salesperson - Enables comparison of
individual sales person performance, identifying top performers and
those needing additional support or training Amount - Provides direct
revenue to measure sales success and a source to set benchmarks across
regions

Product Analysis: Product - Links performance to specific chocolate
types, revealing which items is the main sales driver and which may need
promotional support or discontinuation

Geographic Intelligence: Country - Reveals regional performance
disparities, will provide insighta for resource allocation based on
high-potential markets and identify underperforming territories that
need attention

Temporal Insights: Date - Enables trend analysis to detect seasonality
and growth patterns, which is essential for weekly, monthly, quarterly
or annual sales strategy. The nature of the DD/MM/YYYY format allows for
aggregation by day, month, quarter, or year.

## Section 3: Research Questions & Usage Scenarios

### Usage Scenario

Vinay is a Regional Sales Director at a chocolate company and he wants
to understand what drives sales performance across regions, products,
and his team in order to allocate resources and set targets. He wants to
be able to [explore] transactional sales data in order to [compare]
performance by country, product, and sales person and [identify] top
performers, seasonal trends, and underperforming areas.

When Vinay logs on to our CocoaBoard app, he will see an overview of key
metrics—total sales (\~\$19.79M in the dataset), year-over-year growth
(+54.3%), and breakdowns by Country, Product, and Sales Person. He can
filter by date range, country, or product to compare regions and
individuals, and explore which products and salespeople drive the most
revenue. When he does so, Vinay may e.g. notice that Australia is the
top-performing country and Mallorie Waber is the top sales person, and
that premium dark chocolate variants such as "50% Dark Bites" lead in
sales.

Based on his findings from using our app, Vinay can set regional
targets, reward top performers, rebalance product mix in weaker regions,
and plan seasonal campaigns using the same dashboard for ongoing
monitoring.

### User Stories

*You can choose to frame your detailed requirements as User Stories...*

**User Story 1:** As a **Sales Manager**, I want to **filter sales by
country and date range** in order to **compare regional performance and
spot trends over time**.

**User Story 2:** As a **Regional Sales Director**, I want to **compare
revenue and boxes shipped by product (e.g., 50% Dark Bites, Smooth Silky
Caramel)** in order to **identify best-selling products and adjust
inventory or promotions**.

**User Story 3:** As a **Sales Manager**, I want to **see rankings of
sales people by total sales and by country** in order to **evaluate
individual contribution and allocate territories or incentives**.

**User Story 4:** As a **C-suite executive**, I want to **view
high-level sales trends and YoY growth** in order to **track company
performance and support strategic decisions**.

### Jobs to Be Done

**JTBD 1:** **Situation:** When I am reviewing monthly or quarterly
sales reports... **Motivation:** ...I want to see total sales, growth,
and breakdowns by country and product... **Outcome:** ...so I can align
targets and resource allocation with actual performance.

**JTBD 2:** **Situation:** When evaluating my sales team...
**Motivation:** ...I want to compare sales people by revenue and boxes
shipped, and by region... **Outcome:** ...so I can recognize top
performers and support those in underperforming regions.

**JTBD 3:** **Situation:** When planning product mix and promotions...
**Motivation:** ...I want to see which products sell best in which
countries and over time... **Outcome:** ...so I can prioritize premium
lines (e.g., dark chocolate) and seasonal campaigns.

## Section 5: App Sketch & Description

![Dashboard sketch](img/Dahsboard_sketch.png)
