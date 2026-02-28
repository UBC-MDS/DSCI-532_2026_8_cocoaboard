# Changelog

## [0.2.0] - 2026-02-27

### Added
- Sidebar filters: date range, country, and product inputs
- Three KPI value boxes: Total Revenue, Boxes Shipped, Active Sales Reps
- World map showing revenue by country, color-coded  onscale
- Salesperson leaderboard table with rank, revenue, transactions, and boxes shipped

- `reports/m2_spec.md` with job stories, component inventory, reactivity diagram, and calculation details
- Footer with app description, author names, GitHub repo link, and last updated date
- Two deployments on Posit Connect Cloud: stable (`main`) and preview (`dev`)

### Changed
- `filtered_data()` converted from a plain function to `@reactive.calc` for proper reactive dependency tracking
- YoY % change in value boxes deferred to M3 due to complexity; Revenue Over Time chart planned for M3 instead
- Salesperson leaderboard scope expanded from M1 sketch to include transactions and boxes shipped columns

### Fixed
- `requirements.txt` cleaned to only include packages needed to run the app (removed build tools and Jupyter)

### Known Issues
- Revenue Over Time line chart not yet implemented (planned for M3)
- Map does not support multi-country selection; only one country can be filtered at a time

### Project Tracker
- **Job Story 1** (KPI overview): ✅ Fully implemented — value boxes and filters are live
- **Job Story 2** (salesperson leaderboard): ✅ Fully implemented — leaderboard table with rank, revenue, and boxes shipped
- **Job Story 3** (product mix over time): ⏳ Pending M3 — Revenue Over Time chart deferred
- **Job Story 4** (all metrics update on filter): ✅ Fully implemented — all outputs share a single `@reactive.calc`
- The final layout closely follows the M1 sketch. The main deviation is the absence of the Revenue Over Time line chart, which was replaced temporarily by the leaderboard in M2 and will be added in M3.