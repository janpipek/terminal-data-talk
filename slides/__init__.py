from clippt.slides import slide
from textual.app import App
from rich.console import Console


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

    - supports alternate screen

    """
