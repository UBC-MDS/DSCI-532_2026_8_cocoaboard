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

- App entry point: `src/app.py`.
- Data: `data/raw/Chocolate_Sales.csv` (do not commit large or derived data without team agreement).
- Reports and proposals: `reports/`.
- Use the project’s existing style (e.g. Shiny for Python patterns, descriptive names).

## Questions

If something is unclear, open an issue or contact the contributors listed in the [README](README.md).
