# Changelog

## [0.4.0] - YYYY-MM-DD

Closes [#65](https://github.com/UBC-MDS/DSCI-532_2026_8_cocoaboard/issues/65). Release tracked in [#66](https://github.com/UBC-MDS/DSCI-532_2026_8_cocoaboard/issues/66).

### Added

- Default date range start set to **1 January of the latest year** in the data, so the filter opens with a full-year view (e.g. 2025-01-01 → latest date) instead of the full dataset range. ([#62](https://github.com/UBC-MDS/DSCI-532_2026_8_cocoaboard/issues/62))
- `.env.example` for AI Chat: copy to `.env` and set `ANTHROPIC_API_KEY` to enable the AI Chat tab; see [README](README.md) and [CONTRIBUTING](CONTRIBUTING.md#code-and-project-structure).
- [CONTRIBUTING](CONTRIBUTING.md): M3 collaboration retrospective, M4 norms, and guidelines for adding new components with **modularity** (see [Code and project structure](CONTRIBUTING.md#code-and-project-structure)). ([#64](https://github.com/UBC-MDS/DSCI-532_2026_8_cocoaboard/issues/64))

### Changed

- Date filter default: **start** is now 1 Jan of the max year; **end** remains the latest date. Bounds (min/max) still allow the full data range. ([#62](https://github.com/UBC-MDS/DSCI-532_2026_8_cocoaboard/issues/62))
- CONTRIBUTING expanded with “M3 retrospective and M4 norms” and a clear rule that **`app.py` is the parent** and new widgets/components live in dedicated modules (e.g. `filters.py`, `value_boxes.py`, `query_chat.py`) and are composed in `app.py`. ([#61](https://github.com/UBC-MDS/DSCI-532_2026_8_cocoaboard/issues/61))
- Addressed: modularity refactoring ([#61](https://github.com/UBC-MDS/DSCI-532_2026_8_cocoaboard/issues/61)); date range limits and default ([#62](https://github.com/UBC-MDS/DSCI-532_2026_8_cocoaboard/issues/62)).

### Fixed

- <!-- Bugs resolved since M3. -->

- **Feedback prioritization issue link:** (none this release)

### Known Issues

- AI Chat tab requires `ANTHROPIC_API_KEY`; without it the tab shows a disabled message. On Posit Connect, set the env var in the deployment settings.

### Release Highlight: [Name of your advanced feature]

<!-- One short paragraph describing what you built and what it does for the user. -->

- **Option chosen:** A / B / C / D
- **PR:** #...
- **Why this option over the others:** <!-- 1–2 sentences; link to your feature prioritization issue -->
- **Feature prioritization issue link:** #...

### Collaboration

Summary of workflow and documentation improvements for M4: CHANGELOG and CONTRIBUTING updated per [#65](https://github.com/UBC-MDS/DSCI-532_2026_8_cocoaboard/issues/65) and [#64](https://github.com/UBC-MDS/DSCI-532_2026_8_cocoaboard/issues/64); modularity structure from [#61](https://github.com/UBC-MDS/DSCI-532_2026_8_cocoaboard/issues/61); release tracked in [#66](https://github.com/UBC-MDS/DSCI-532_2026_8_cocoaboard/issues/66).

- **CONTRIBUTING.md:** [CONTRIBUTING](CONTRIBUTING.md#m3-retrospective-and-m4-norms) updated with M3 retrospective and M4 norms. ([#64](https://github.com/UBC-MDS/DSCI-532_2026_8_cocoaboard/issues/64))
- **M3 retrospective:** What worked: clear job stories and component inventory ([m2_spec](reports/m2_spec.md)), splitting dashboard vs. AI tab, fixing layout (e.g. `page_navbar`) before adding features. What didn’t: layout/head-content bugs were hard to debug; testing filter reactivity right after layout changes would have helped. Full notes in [CONTRIBUTING](CONTRIBUTING.md#m3-retrospective-and-m4-norms).
- **M4:** Documented modularity norms ([#61](https://github.com/UBC-MDS/DSCI-532_2026_8_cocoaboard/issues/61)): new UI/server logic in dedicated modules; `app.py` as single parent that wires data and composes panels; run the app after changes; use PRs for decisions.

### Reflection

<!-- Standard (see General Guidelines): what the dashboard does well, current limitations,
     any intentional deviations from DSCI 531 visualization best practices. -->

<!-- Trade-offs: one sentence on feedback prioritization - full rationale is in #<issue> and ### Changed above. -->

<!-- Most useful: which lecture, material, or feedback shaped your work most this milestone,
     and anything you wish had been covered. -->

---

## [0.3.0] - 2026-03-07

### Added
- Three new KPI value boxes: Average Revenue (filtered), Year-over-Year Revenue %, Month-over-Month Revenue %
- Revenue trend line chart showing monthly revenue for the top 5 sales reps (responds to all filters)
- YoY and MoM cards respond to country and product filters but ignore the date range, so they always compare full time periods

### Changed
- Default date range updated from a single month (Aug 2024) to the full latest year (Jan–Aug 2024). The previous single-month default left the revenue trend chart empty and gave a narrow view of KPIs. A full-year default provides meaningful trend data, actionable KPI context, and a better first impression of the dashboard. Country and product filters default to "All" to maximize the initial data scope.

### Fixed
- Footer was hidden behind dashboard widgets due to `page_fillable` stretching the viewport; switched to `page_navbar` layout so the footer always renders below content 
- Country and product filters were single-select with an "All" option; replaced with `multiple=True` so the default empty selection means all data is shown and user is able to select multiple options.
- Map can now support multi-country filtering via the updated multi-select country filter 

### Reflection
- **Job Story 1** (KPI overview): ✅ Fully implemented — three new KPI boxes added for Avg Revenue, YoY %, and MoM %, giving users richer more essential context beyond totals with benchmarks
- **Job Story 2** (filter reactivity): ✅ Improved — multi-select filters now let users able to compare multiple countries and products simultaneously (the M2 single-select limitation is resolved)
- **Job Story 3** (choropleth map): ✅ Improved — map now responds to multi-country selection
- **Job Story 4** (salesperson leaderboard): ✅ Enhanced — two new columns added (Avg Deal Size and Revenue Share %) to give more insights about each sales rep
- **AI Tab**: ✅ New in M3 — querychat integration with Claude allows natural language filtering of the chocolate sales data, with a reactive dataframe, choropleth, top sales reps chart, and CSV download all responding to the AI-filtered results
- The M2 dashboard issues were all solved in M3, with an additional new AI natural language filtering tab. More insights were offered comparing to the M2 dashborad with more comparison metrics and charts over the sales rep performance. The main challenge this milestone was the `page_navbar` head content bug, which caused subtle reactivity failures that were non-obvious to debug. Moving forward, any Shiny layout changes should be tested immediately against filter reactivity before building further on top.

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
- Changed the way packages are getting imported because it was breaking on posit cloud connect
- `filtered_data()` converted from a plain function to `@reactive.calc` for proper reactive dependency tracking
- YoY % change in value boxes deferred to M3 due to complexity; Revenue Over Time chart planned for M3 instead
- Salesperson leaderboard scope expanded from M1 sketch to include transactions and boxes shipped columns

### Fixed
- `requirements.txt` cleaned to only include packages needed to run the app (removed build tools and Jupyter)

### Known Issues
- Revenue Over Time line chart not yet implemented (planned for M3)
- Map does not support multi-country selection; only one country can be filtered at a time

### Reflection
- **Job Story 1** (KPI overview): ✅ Fully implemented — value boxes and filters are live
- **Job Story 2** (filter reactivity): ✅ Fully implemented — all outputs share a single `@reactive.calc` and update simultaneously
- **Job Story 3** (choropleth map): ✅ Fully implemented — world map colored by country revenue responds to product and date filters
- **Job Story 4** (salesperson leaderboard): ✅ Fully implemented — leaderboard table with rank, revenue, transactions, and boxes shipped
- All 4 job stories for M2 are fully implemented. The final layout closely follows the M1 sketch. The main deviation is the absence of a Revenue Over Time line chart from the original proposal, which is deferred to M3.
