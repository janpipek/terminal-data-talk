from rich.console import Console
from textual.app import App
from textual.containers import Container, VerticalScroll
from textual.widgets import Markdown, DataTable

from clippt.slides import slide
from dynamic_slides.dashboard import weather_dashboard
from textwrap import dedent


@slide
def terminal_is_your_weapon(app: App):
    dims = app.size

    console = Console()
    console.color_system

    return f"""\
    ## (Modern) Terminal emulator is your weapon

    - reports size: *{dims.width}* x *{dims.height}*

    - supports colours: {console.color_system}

    - supports ASCII:

        \\* # o . - | x

    - supports Unicode symbols:

        │ ─┌ ┐ └ ┘ ┼ ┴ ┬ █

    - ...including emoji

        🖖 💕 👽 🦖 💯

    - supports alternate screen

    """


@slide
def data_table(app: App):
    md = Markdown(dedent("""
        # DataTable widget

        ```
        dt = DataTable()
        dt.add_columns("a", "b", "c")
        dt.add_row(["1", "2", "3"])
        ```
    """)
    )
    dt = DataTable()
    dt.add_columns("a", "b", "c")
    dt.add_row("1", "2", "3")
    dt.add_row("4", "5", "6")
    return VerticalScroll(
        md,
        dt,
        can_focus=False,
        can_focus_children=False,
    )



__all__ = ["weather_dashboard", "terminal_is_your_weapon", "data_table"]
