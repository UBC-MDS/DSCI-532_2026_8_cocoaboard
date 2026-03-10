# Contributing to CocoaBoard

Thanks for your interest in contributing. Here’s how to get set up and submit changes.

## Development setup

1. Clone the repo and enter the project directory.
2. Create and activate the conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate cocoaboard
   ```
3. Run the app locally to confirm everything works:
   ```bash
   shiny run src/app.py
   ```
   For development with auto-reload on file changes, use:
   ```bash
   shiny run src/app.py --reload
   ```
   Optionally open the app in your browser automatically:
   ```bash
   shiny run src/app.py --reload --launch-browser
   ```

## How to contribute

- **Bugs and ideas:** Open an issue describing the problem or feature and how to reproduce it (for bugs).
- **Code changes:** Use a new branch, make your changes, then open a pull request (PR) against `main`.

## Pull request guidelines

- Keep changes focused (one feature or fix per PR when possible).
- Ensure the app still runs with `shiny run src/app.py`.
- Update the README or docs if you change setup or usage.
- Request review from a maintainer; address feedback before merging.

## Code and project structure

- **App entry point:** `src/app.py` is the **parent** — it loads data, defines reactive calcs, and composes the UI and server. It should stay focused on wiring and orchestration, not on fine-grained widget or chart logic.
- **Modularity:** New components and widgets belong in **dedicated modules**, not in `app.py`. Add UI-building functions and (when it makes sense) small helpers in the appropriate file:
  - **Filters:** `src/filters.py` — date range, country, product (and any new filter widgets).
  - **Dashboard layout:** `src/dashboard.py` — composes filters, value boxes, map, leaderboard, revenue trend, footer for the main tab.
  - **Charts and tables:** `src/map_chart.py`, `src/leaderboard.py`, `src/revenue_trend.py`, `src/value_boxes.py` — each owns one main visualization or block.
  - **AI Chat:** `src/query_chat.py` — QueryChat setup and AI Chat tab UI.
  - **Shared bits:** `src/theme.py` (styling/head content), `src/constants.py` (e.g. country codes, URLs), `src/footer.py` (footer UI).
- **Import pattern:** Use the existing pattern in `app.py`: relative imports when run as `src.app` (e.g. on Posit Connect) and absolute imports when run as a script (`shiny run src/app.py`). New modules should be imported in `app.py` and composed there; they should not import each other in a circular way.
- **Data:** `data/raw/Chocolate_Sales.csv` (do not commit large or derived data without team agreement).
- **Reports and proposals:** `reports/`.
- Use the project’s existing style (e.g. Shiny for Python patterns, descriptive names).

## M3 retrospective and M4 norms

### M3 retrospective

- **What worked:** Having clear job stories and a component inventory (e.g. in `reports/m2_spec.md`) made it easier to implement and review. Splitting the dashboard tab and the AI Chat tab kept scope clear. Fixing the layout (e.g. moving to `page_navbar` and fixing head content) before adding more features avoided compounding bugs.
- **What didn’t:** Layout and head-content issues were subtle and time-consuming to debug because of lack of modularity; reactivity looked correct in some places but failed in others. Testing filter reactivity right after any layout change would have caught this earlier. Modularity within the components would have made it easier for debugging.

### M4 norms

- **Add features with modularity in mind:** New widgets and panels go in the right module (see [Code and project structure](#code-and-project-structure)); `app.py` stays the single place that wires data and composes panels.
- **Run the app after changes:** Always run `shiny run src/app.py` (or `--reload`) to confirm the app still works and filters/charts update as expected.
- **Decisions on record:** Non-trivial process or structure decisions (e.g. default date range, env vars, collaboration norms) are documented in CONTRIBUTING or CHANGELOG and agreed via a PR when possible.

## Questions

If something is unclear, open an issue or contact the contributors listed in the [README](README.md).
