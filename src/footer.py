"""Footer component for CocoaBoard."""

from shiny import ui


def footer_ui():
    """Return the app footer with credits and repo link."""
    return ui.tags.footer(
        "CocoaBoard | Created by Daisy Zhou, Vinay Valson, Eduardo Rivera | ",
        ui.tags.a(
            "GitHub Repo",
            href="https://github.com/UBC-MDS/DSCI-532_2026_8_cocoaboard",
            target="_blank",
        ),
        " | Last updated: March 2026",
        style=(
            "text-align: center; padding: 1rem; margin-top: 2rem; "
            "font-size: 0.85rem; color: #666; border-top: 1px solid #C4A35A;"
        ),
    )
