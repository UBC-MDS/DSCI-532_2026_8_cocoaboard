# Project Proposal for Chocolate Sales Dashboard

## Section 1: Motivation and Purpose

### Target Audience

Our target audience will be primarity Sales Managers, Regional Sales Directors or C-suites at a chocolate manufacturing/distribution company. Our team will serve as Data Analytics Consultants for the sales team providing actionable insights to help the leadership team optimize their sales strategy and resource allocation.

### Problem
Here are the challengs facing by the chocolate company:

- Inconsistent sales performance across regions and salespeople: need to build performance tracker for sales strategy and human resource training 
- Inefficient product mix decisions: need to discover the top product sales for efficient recource allocation
- Reactive rather than proactive management: Monthly or quarterly reviews happen too late to course-correct, and they need real-time visibility into trends
- Missed opportunities: need to identify seasonal patterns, top customers, or which salesperson-product combinations work best

### Solution
Our interactive R Shiny dashboard will serve as a centralized, web-based command center accessible from any browser. Through intuitive dropdown filters, date selectors, and dynamic visualizations, sales managers can instantly compare performance across salespeople, products, and countries without technical expertise. 

Interactive charts reveal trends over time, highlight top and underperforming segments, and calculate profit margins on-the-fly. Users can drill down from high-level overviews to granular transaction details, answer ad-hoc questions independently, and even generate personalized performance views for individual sales reps. This self-service analytics tool transforms static data into actionable intelligence, enabling the team to shift from reactive quarterly reviews to proactive, data-driven decision-making in real-time.

## Section 2: Description of the Data

### Stats
The Chocolate Sales dataset contains 6 columns and provides transactional-level sales data across multiple dimensions.

Columns:
Salesperson - The name of the salesperson responsible for the sale.
Country - The country where the sale was made.
Product - The name and type of the product sold.
Date - The date when the sale transaction occurred (DD/MM/YYYY format).
Amount - The total sales amount for the transaction, expressed in US dollars.
Boxes Shipped- The number of product boxes shipped as part of the transaction.

### Relevance
Performance Tracking Variables:
Salesperson - Enables comparison of individual sales person performance, identifying top performers and those needing additional support or training
Amount - Provides direct revenue to measure sales success and a source to set benchmarks across regions

Product Analysis:
Product - Links performance to specific chocolate types, revealing which items is the main sales driver and which may need promotional support or discontinuation

Geographic Intelligence:
Country - Reveals regional performance disparities, will provide insighta for resource allocation based on high-potential markets and identify underperforming territories that need attention

Temporal Insights:
Date - Enables trend analysis to detect seasonality and growth patterns, which is essential for weekly, monthly, quarterly or annual sales strategy. The nature of the DD/MM/YYYY format allows for aggregation by day, month, quarter, or year.
