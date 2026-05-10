import os
from pathlib import Path

import click
from clippt import Presentation, PresentationApp
from clippt.slides import MarkdownSlide, ShellSlide, load_slide

from .dynamic_slides import (
    terminal_is_your_weapon,
    weather_dashboard,
)

CWD = Path(__file__).parent.parent


@click.command()
@click.option(
    "--continue", "-c", "continue_", is_flag=True, help="Continue from last slide."
)
@click.option("--disable-footer", is_flag=True, help="Disable footer.")
def presentation(continue_: bool, disable_footer: bool):
    """Run the presentation."""
    os.chdir(CWD)
    presentation = create_presentation()
    app = PresentationApp(presentation)
    app.enable_footer = not disable_footer
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
        load("slides/000-title.md", classes=["title"]),
        # "slides/001-prompt.md",
        "slides/001-prompt2.md",
        "slides/001-prompt3.md",
        md("# Why?"),
        "slides/004-why.md",
        md("# Python in the terminal...\n...is just Python 🐍"),
        "slides/010-problems.md",
        # Tabular data
        md("# Tabular data"),
        # md("slides/100-tabular.md"),
        "data/countries.csv",
        # sh("cat data/countries.csv", title="data/countries.csv", mode="output"),
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
        # sh("bat data/countries.csv --paging=never", title="bat = cat & less on steroids ⛏️"),
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
        # "data/cities.parquet",
        load("slides/143-polars_cities.py", alt_screen=True, wait_for_key=True),
        load(
            "slides/143-rich_cities.py",
            alt_screen=True,
            wait_for_key=True,
            runnable=False,
        ),
        md("# Let's get interactive...\n\nor just wait a bit"),
        # Visualisation
        "slides/200-visualisation.md",
        # "slides/spurious_correlations.csv",
        terminal_is_your_weapon,
        md("# Example: Simple barchart\nThe most populous countries in Asia"),
        "slides/simple_bar.py",
        load("slides/simple_bar_unicode.py", mode="output"),
        load("slides/simple_bar_unicode2.py", mode="output"),
        "slides/colours.md",
        load("slides/colours1.py", title="Apply ANSI escape codes"),
        load("slides/colours256.py", title="256 colours"),
        # load("slides/true_colour.py", mode="output", title="True colour"),
        load("slides/simple_bar_colours.py", title="Pinch of colours"),
        md("# Example: Simple scatter plot to draw a 'map' of Czechia"),
        load("slides/simple_scatter.py"),
        md("# Aren't we reinventing the wheel?"),
        "slides/libraries.md",
        "slides/plottile.md",
        load("slides/plotille_line.py"), #, alt_screen=True, wait_for_key=True),
        load("slides/plotille_hist.py"),
        "slides/plotext.md",
        load("slides/plotext_line.py"),
        # load("slides/spurious_correlations.py"),
        load("slides/plotext_hist.py"),
        md("# What if..."),
        md("# ...we could actually use matplotlib in the terminal?\nkitty save us!"),
        load("slides/kitty.py", alt_screen=True, wait_for_key=True),
        # Dashboards
        "slides/400-dashboards.md",
        sh("htop", alt_screen=True),
        md("# Don't reinvent the wheel!"),
        "slides/textual.md",
        "slides/textual-widgets.md",
        "slides/textual-fastdatatable.md",
        load("slides/data_viewer.py", alt_screen=True, wait_for_key=False),
        "slides/textual-plotext.md",
        "data/weather.parquet",
        weather_dashboard,
        # End
        load("slides/999-end.md", classes=["title"]),
    ]

    return Presentation(
        title="Data wrangling in a modern terminal",
        slides=[load_slide(s) if isinstance(s, str) else s for s in slides],
    )


if __name__ == "__main__":
    presentation()
