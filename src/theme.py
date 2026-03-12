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
  box-shadow: 0 4px 12px rgba(45, 24, 16, 0.12) !important;
  overflow: visible !important;
  transition: box-shadow 0.2s ease, transform 0.2s ease !important;
  position: relative;
}
.bslib-card:hover, .card:hover {
  box-shadow: 0 8px 24px rgba(45, 24, 16, 0.16) !important;
}
.bslib-card .card-body, .card .card-body {
  overflow: visible !important;
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
/* Map and chart cards: white background with shadow and hover */
.card-bg-white {
  background: white !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
  transition: box-shadow 0.2s ease !important;
}
.card-bg-white:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.14) !important;
}
.card-bg-white .card-header {
  background: white !important;
  border-bottom: 1px solid #dee2e6 !important;
}
/* Auto height based on widget content (value boxes and standalone cards only) */
.bslib-card, .card {
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
/* Layout: columns and rows size to content, no stretch; allow dropdowns to overflow */
.bslib-grid, .bslib-fill-container, [class*="layout-columns"] {
  align-items: start !important;
  overflow: visible !important;
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

/* Subtle loader overlay with spinner on main widgets while app is busy */
.shiny-busy .card-bg-white::after,
.shiny-busy .bslib-value-box::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.shiny-busy .card-bg-white::before,
.shiny-busy .bslib-value-box::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 2.25rem;
  height: 2.25rem;
  margin-top: -1.125rem;
  margin-left: -1.125rem;
  border-radius: 50%;
  border: 3px solid rgba(93, 58, 26, 0.25);
  border-top-color: var(--chocolate-medium);
  animation: cocoa-spin 0.8s linear infinite;
  z-index: 11;
}

@keyframes cocoa-spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Consistent sidebar width across tabs (Dashboard + AI Chat Helper) */
.bslib-sidebar-layout .bslib-sidebar {
  width: 360px !important;
  flex: 0 0 360px !important;
  max-width: 360px !important;
}

/* Year radio buttons styled as a button group */
.year-buttons .shiny-input-radiogroup {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
}
.year-buttons .form-check {
  margin: 0 !important;
  padding: 0 !important;
}
.year-buttons .form-check-input {
  display: none !important;
}
.year-buttons .form-check-label {
  display: inline-block;
  padding: 0.35rem 0.6rem;
  border: 1px solid var(--chocolate-light);
  border-radius: 8px;
  background: #FFFEFB;
  color: var(--chocolate-dark);
  cursor: pointer;
  user-select: none;
}
.year-buttons .form-check-input:checked + .form-check-label {
  background: var(--chocolate-medium);
  border-color: var(--chocolate-medium);
  color: #fff;
}
.year-buttons .form-check-label:hover {
  border-color: var(--chocolate-medium);
}
"""


_MAP_CLICK_LISTENER_JS = """
window.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'cocoa_map_click') {
        Shiny.setInputValue('map_clicked_country', event.data.country, {priority: 'event'});
    }
});
"""


def get_head_content():
    """Return head content: Bootstrap Icons, chocolate theme CSS, and map click listener."""
    return head_content(
        ui.tags.link(
            rel="stylesheet",
            href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.11.3/font/bootstrap-icons.min.css",
        ),
        ui.tags.style(CHOCOLATE_CSS),
        ui.tags.script(_MAP_CLICK_LISTENER_JS),
    )
