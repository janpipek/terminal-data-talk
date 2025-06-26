import click

from clippt import PresentationApp, md


TITLE = "Data wrangling in a modern terminal"

SLIDES = [
    md("slides/000-title.md"),
    md("slides/001-prompt.md"),
    md("slides/001-prompt2.md"),
    md("slides/001-prompt3.md"),
    md("slides/010-content.md"),
]


@click.command()
def presentation():
    """Start the presentation app."""
    app = PresentationApp(
        title=TITLE,
        slides=SLIDES,
    )
    app.run()


if __name__ == "__main__":
    presentation()