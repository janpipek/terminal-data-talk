from pathlib import Path

import click

from clippt import PresentationApp, md, sh, py
from dashboard import weather_dashboard


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
    md("# Python in the terminal...\n...is just Python"),
    "slides/010-problems.md",

    # Tabular data
    md("slides/100-tabular.md"),
    "data/countries.csv",
    # sh("cat data/countries.csv", title="data/countries.csv", mode="output"),
    sh("cat data/countries.csv | less", alt_screen=True, title="Standard Unix tool: cat"),
    sh("bat data/countries.csv", alt_screen=True, title="bat = cat on steroids"),
    "slides/120-task-sort.md",
    "slides/121-countries_by_population.py",
    sh("xan view -A data/countries.csv", title="xan = The CSV magician"),
    sh("xan sort -NR -s population data/countries.csv | xan view"),
    sh("xan search -s region Asia data/countries.csv  | xan sort -NR -s population | xan view"),
    "data/cities.parquet",
    sh("bat data/cities.parquet", alt_screen=True),
    "slides/130-visidata.md",
    sh("visidata data/countries.csv", alt_screen=True),

    # Visualisation
    "slides/200-visualisation.md",

    # Dashboards
    "slides/400-dashboards.md",
    sh("htop", alt_screen=True),
    weather_dashboard,

    # End
    "slides/999-end.md",
]


if __name__ == "__main__":
    presentation()
