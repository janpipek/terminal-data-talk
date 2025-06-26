import click

from clippt import PresentationApp, md


TITLE = "Data wrangling in a modern terminal"

SLIDES = [
    md("slides/000-title.md"),
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