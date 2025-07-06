from pathlib import Path

import click

from clippt import PresentationApp, load, md, sh
from dynamic_slides import terminal_is_your_weapon, weather_dashboard


@click.command()
@click.option(
    "--continue", "-c", "continue_", is_flag=True, help="Continue from last slide."
)
def presentation(continue_: bool):
    """Run the presentation."""
    app = PresentationApp(
        title=TITLE,
        slides=SLIDES,
    )
    if continue_ and Path(".current_slide").exists():
        app.slide_index = int(Path(".current_slide").read_text())
    app.slide_index = min(app.slide_index, len(SLIDES) - 1)
    app.run()


TITLE = "Data wrangling in a modern terminal"

SLIDES = [
    # Intro
    "slides/000-title.md",
    "slides/001-prompt.md",
    "slides/001-prompt2.md",
    "slides/001-prompt3.md",
    md("# Why?"),
    "slides/004-why.md",
    md("# Python in the terminal...\n...is just Python 🐍"),
    "slides/010-problems.md",
    # Tabular data
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
    sh("xan view -A data/countries.csv", title="xan = The CSV magician ⛏️"),
    sh("xan sort -NR -s population data/countries.csv | xan view -M"),
    sh(
        "xan search -s region Asia data/countries.csv  | xan sort -NR -s population | xan view -M"
    ),
    "slides/130-visidata.md",
    sh("visidata data/countries.csv", alt_screen=True),
    md("# Enough shell...\nlet's Python"),
    "slides/121-sorted_countries_pandas.py",
    "slides/122-sorted_countries_polars.py",
    "slides/140-rich.md",
    "slides/141-rich.py",
    "slides/142-rich_countries.py",
    "data/cities.parquet",
    load("slides/143-polars_cities.py", alt_screen=True, wait_for_key=True),
    load(
        "slides/143-rich_cities.py", alt_screen=True, wait_for_key=True, runnable=False
    ),
    md("# Let's get interactive...\n\nor just wait a bit"),
    # Visualisation
    "slides/200-visualisation.md",
    load(
        "slides/spurious_correlations.py",
        title="Czech jet fuel consumption vs successful climbs of Mt. Everest\n\n",
        mode="output",
    ),
    # "slides/spurious_correlations.csv",
    terminal_is_your_weapon,
    # Dashboards
    "slides/400-dashboards.md",
    sh("htop", alt_screen=True),
    weather_dashboard,
    # End
    "slides/999-end.md",
]


if __name__ == "__main__":
    presentation()
