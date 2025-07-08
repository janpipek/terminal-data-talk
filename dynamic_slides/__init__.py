from rich.console import Console
from textual.app import App

from clippt.slides import slide
from dynamic_slides.dashboard import weather_dashboard


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


__all__ = ["weather_dashboard", "terminal_is_your_weapon"]
