# Project Proposal for Chocolate Sales Dashboard

## Section 1: Motivation and Purpose

### Target Audience

Our target audience will be primarity Sales Managers, Regional Sales Directors or C-suites at a chocolate manufacturing/distribution company. Our team will serve as Data Analytics Consultants for the sales team providing actionable insights to help the leadership team optimize their sales strategy and resource allocation.

### Problem

Here are the challengs facing by the chocolate company:

- Inconsistent sales performance across regions and salespeople 
- Inefficient product mix decisions 
- Reactive rather than proactive management - Monthly or quarterly reviews happen too late to course-correct, and they need real-time visibility into trends
- Missed opportunities - They can't easily identify seasonal patterns, top customers, or which salesperson-product combinations work best

### Solution

Creating machine learning models often involves writing redundant code, particularly when tuning hyperparameters and comparing performance across different models. This project aims to reduce that redundancy by streamlining these repetitive steps, making the model development process more efficient and time-effective. To achieve this, our project focuses on building reusable functions that, given user input, automatically return the optimal hyperparameters, the best-performing model, its accuracy score, and a corresponding confusion matrix, all in a single, unified workflow.

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
Salesperson - Enables comparison of individual sales performance, identifying top performers and those needing support or training.
Boxes and Amount - Provide volume and revenue metrics to measure success and set benchmarks

Profitability Analysis:
Cost per box - Combined with Amount, allows calculation of profit margins and identification of high-value products
Product - Links performance to specific items, revealing which products drive profitability versus just volume

Geographic Intelligence:

Country - Reveals regional performance disparities, helping allocate resources to high-potential markets and identify underperforming territories

Temporal Insights:

Date - Enables trend analysis to detect seasonality, growth patterns, and timing of successful campaigns

Strategic Combinations:
The real power lies in cross-referencing these variables:

Salesperson × Product = Which reps excel at selling premium items?
Country × Date = Are there regional seasonal patterns?
Product × Boxes × Amount = Which products have the best revenue-per-box ratio?
Salesperson × Country = Should we reassign territories based on performance?

This multidimensional dataset provides all the necessary inputs to transform the sales team's reactive approach into a proactive, data-driven strategy.
