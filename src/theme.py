"""Chocolate theme styles and head content for the dashboard."""

from htmltools import head_content
from shiny import ui

CHOCOLATE_CSS = """
:root {
  --chocolate-dark: #2C1810;
  --chocolate-medium: #5D3A1A;
  --chocolate-milk: #8B6914;
  --chocolate-light: #C4A35A;
  --cream: #F5E6D3;
  --cream-dark: #E8D4BC;
  --caramel: #D4A574;
}
body {
  background: linear-gradient(135deg, #FDF8F0 0%, #F5E6D3 50%, #E8D4BC 100%) !important;
  color: var(--chocolate-dark) !important;
  font-family: "Segoe UI", system-ui, sans-serif;
}
h1, h2, h3, h4, .card-header {
  color: var(--chocolate-dark) !important;
  font-weight: 600;
}
.bslib-card, .card {
  background-color: rgba(255, 251, 245, 0.95) !important;
  border: 1px solid var(--chocolate-light) !important;
  border-radius: 10px !important;
  box-shadow: 0 2px 8px rgba(45, 24, 16, 0.08) !important;
}
.bslib-card-header, .card-header {
  background: linear-gradient(180deg, var(--cream-dark) 0%, var(--cream) 100%) !important;
  border-bottom: 1px solid var(--chocolate-light) !important;
  color: var(--chocolate-dark) !important;
  font-weight: 600;
  border-radius: 10px 10px 0 0 !important;
}
.bslib-value-box {
  background: linear-gradient(135deg, var(--cream) 0%, #FFF8F0 100%) !important;
  border: 1px solid var(--chocolate-light) !important;
  border-radius: 10px !important;
  box-shadow: 0 2px 8px rgba(45, 24, 16, 0.06) !important;
}
.bslib-value-box .value-box-title {
  color: var(--chocolate-medium) !important;
}
.bslib-value-box .value-box-value {
  color: var(--chocolate-dark) !important;
}
.form-control, .form-select {
  border-color: var(--chocolate-light) !important;
  background-color: #FFFEFB !important;
}
.form-control:focus, .form-select:focus {
  border-color: var(--chocolate-medium) !important;
  box-shadow: 0 0 0 0.2rem rgba(93, 58, 26, 0.2) !important;
}
/* Auto height based on widget content */
.bslib-card, .card {
  height: auto !important;
  min-height: 0 !important;
}
.bslib-value-box {
  height: auto !important;
  min-height: 0 !important;
}
.bslib-value-box .card-body {
  min-height: 0 !important;
}
.form-control, .form-select, .selectize-input {
  height: auto !important;
  min-height: 2.25rem !important;
}
/* Layout: columns and rows size to content, no stretch */
.bslib-grid, .bslib-fill-container, [class*="layout-columns"] {
  align-items: start !important;
}
.bslib-grid > *, .bslib-fill-container > * {
  height: auto !important;
  min-height: 0 !important;
}
/* Page fillable: let content determine height */
.shiny-fill-container {
  min-height: 0 !important;
  height: auto !important;
}
"""


def get_head_content():
    """Return head content: Bootstrap Icons and chocolate theme CSS."""
    return head_content(
        ui.tags.link(
            rel="stylesheet",
            href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.11.3/font/bootstrap-icons.min.css",
        ),
        ui.tags.style(CHOCOLATE_CSS),
    )
