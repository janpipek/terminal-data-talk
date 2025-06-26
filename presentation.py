from pathlib import Path

import click

from clippt import PresentationApp, md, sh, py


TITLE = "Data wrangling in a modern terminal"

SLIDES = [
    md("slides/000-title.md"),
    md("slides/001-prompt.md"),
    md("slides/001-prompt2.md"),
    md("slides/001-prompt3.md"),
    md("slides/010-content.md"),
    md("slides/100-tabular.md"),
    md("slides/120-xan.md"),
    md("slides/130-visidata.md"),
    sh("uv run visidata", requires_alt_screen=True),
    md("slides/200-visualisation.md"),
    md("slides/400-dashboards.md"),
    md("slides/999-end.md"),
]


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


if __name__ == "__main__":
    presentation()