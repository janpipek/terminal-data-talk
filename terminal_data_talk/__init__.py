import os
from pathlib import Path

import click
from clippt import Presentation, PresentationApp
from clippt.slides import MarkdownSlide, ShellSlide, load_slide

from .dynamic_slides import (
    europython_logo,
    terminal_is_your_weapon,
    weather_dashboard,
)

CWD = Path(__file__).parent.parent


@click.command()
@click.option(
    "--continue", "-c", "continue_", is_flag=True, help="Continue from last slide."
)
@click.option("--disable-footer", is_flag=True, help="Disable footer.")
@click.option("--disable-header", is_flag=True, help="Disable header.")
def presentation(continue_: bool, disable_footer: bool, disable_header: bool):
    """Run the presentation."""
    os.chdir(CWD)
    presentation = create_presentation()
    app = PresentationApp(presentation)
    app.theme = "atom-one-light"  # Make this configurable at the library side
    app.enable_footer = not disable_footer
    app.enable_header = not disable_header
    if continue_ and Path(".current_slide").exists():
        current_slide_index = int(Path(".current_slide").read_text())
    else:
        current_slide_index = 0
    app.slide_index = min(current_slide_index, len(presentation.slides) - 1)
    app.run()


def create_presentation():
    def md(source, *, title=None):
        return MarkdownSlide(source=source, title=title)

    def sh(command, **kwargs):
        return ShellSlide(source=command, cwd=CWD, **kwargs)

    def load(source, **kwargs):
        return load_slide(source, **kwargs)

    slides = [
        # ---- Intro ----
        europython_logo,
        load("slides/000-title.md", classes=["title"]),
        "slides/004-why.md",
        md("# You are already in the command line..."),
        sh("ssh me@elsewhe.re", runnable=False),
        load("slides/007-mandelbrot.py"),q
        sh("Be cool!😎 \ncmatrix # HIDE", alt_screen=True, display_mode="output"),
        md("# Python in the terminal...\n...is just Python"),
        "slides/010-problems.md",
        # ---- Tabular data ----
        md("# Tabular data"),
        # "data/countries.csv",
        sh(
            "cat data/countries.csv | less",
            alt_screen=True,
            title="Standard Unix tools: cat, less ⛏️",
        ),
        sh(
            "bat data/countries.csv",
            alt_screen=True,
            title="bat = cat & less on steroids ⛏️",
        ),
        "slides/120-task-sort.md",
        md("# xan = The CSV magician ⛏️"),
        sh("xan view -A data/countries.csv"),
        sh("xan sort -NR -s population data/countries.csv | xan view -M"),
        sh(
            "xan search -s region Asia data/countries.csv  | xan sort -NR -s population | xan view -M"
        ),
        "slides/130-visidata.md",
        sh("visidata data/countries.csv", alt_screen=True),
        md("# Enough external tools...\nlet's Python"),
        "slides/121-sorted_countries_pandas.py",
        "slides/122-sorted_countries_polars.py",
        "slides/140-rich.md",
        "slides/141-rich.py",
        "slides/142-rich_countries.py",
        load("slides/143-polars_cities.py", alt_screen=True, wait_for_key=True),
        load(
            "slides/143-rich_cities.py",
            alt_screen=True,
            wait_for_key=True,
            runnable=False,
        ),
        # ---- Visualisation ----
        "slides/200-visualisation.md",
        terminal_is_your_weapon,
        md("# Example: Simple barchart\nThe most populous countries in Asia"),
        "slides/210-simple_bar.py",
        load("slides/211-simple_bar_unicode.py", mode="output"),
        load("slides/212-simple_bar_unicode2.py", mode="output"),
        "slides/220-colours.md",
        load("slides/221-colours1.py", title="Apply ANSI escape codes"),
        load("slides/222-colours256.py", title="256 colours"),
        load("slides/223-simple_bar_colours.py", title="Pinch of colours"),
        md("# Example: Simple scatter plot to draw a 'map' of Poland"),
        load("slides/231-simple_scatter.py"),
        md("# Example: Topographic map of Poland"),
        load("slides/240-map.py"),
        md("# Aren't we reinventing the wheel?"),
        "slides/301-libraries.md",
        "slides/310-plottile.md",
        load("slides/311-plotille_line.py"),
        load("slides/312-plotille_hist.py"),
        "slides/320-plotext.md",
        load("slides/321-plotext_line.py"),
        load("slides/322-plotext_hist.py"),
        md("# What if..."),
        md("# ...we could actually use matplotlib in the terminal?\nkitty save us!"),
        load("slides/332-kitty.py", alt_screen=True, wait_for_key=True),
        # ---- Dashboards ---
        "slides/400-dashboards.md",
        sh("htop", alt_screen=True),
        md("# Don't reinvent the wheel!"),
        "slides/410-textual.md",
        "slides/411-textual-widgets.md",
        "slides/412-textual-fastdatatable.md",
        load("slides/420-data_viewer.py", alt_screen=True, wait_for_key=False),
        "slides/430-textual-plotext.md",
        md("# Example: Temperature dashboard (Kraköw)"),
        "data/krakow-meteostat.parquet",
        weather_dashboard,
        # ---- End ----
        load("slides/999-end.md", classes=["title"]),
    ]

    return Presentation(
        title="Data wrangling in a modern terminal",
        slides=[load_slide(s) if isinstance(s, str) else s for s in slides],
        slide_base_path=Path(".")
    )


if __name__ == "__main__":
    presentation()
