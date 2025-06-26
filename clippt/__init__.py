import io
import os
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from textwrap import dedent
from dataclasses import dataclass, field
from typing import Optional, ClassVar, Literal, Callable

import click
import rich
from rich.text import Text
from rich.console import Console
from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widget import Widget
from textual.widgets import Footer, Markdown, Static
from rich.panel import Panel
from textual.css.query import QueryError

from typing import Any

from clippt.defaults import my_theme, css_tweaks


class PresentationApp(App):
    """A Textual app for the presentation."""

    enable_footer: bool = True

    BINDINGS = [
        ("pageup", "prev_slide", "Previous"),
        ("pagedown", "next_slide", "Next"),
        (".", "run", "Run"),
        ("q", "quit", "Quit"),
        ("home", "home", "First slide"),
        ("e", "edit", "Edit"),
        ("r", "reload", "Reload"),
        # ("s", "shell", "Shell"),
        # ("d", "toggle_dark", "Toggle dark mode")
    ]
    
    CSS = css_tweaks

    slide_index: int = 0

    slides: list["Slide"]

    document_title: str

    def __init__(self, *, slides: list, title: str, **kwargs):
        self.slides = slides
        self.document_title = title
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        # yield Header(show_clock=True)
        yield VerticalScroll(
            Markdown("Loading..."), id="content", can_focus=False
        )
        if self.enable_footer:
            yield Footer()

    def on_mount(self) -> None:
        """Hook called when the app is mounted."""
        self.register_theme(my_theme)
        self.theme = "my"
        self.update_slide()

    def on_resize(self) -> None:
        """Hook called when the app is resized."""
        self.update_slide()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_reload(self) -> None:
        self.current_slide.reload()
        self.update_slide()

    def action_next_slide(self) -> None:
        self.switch_to_slide(min(self.slide_index + 1, len(self.slides) - 1))

    def action_prev_slide(self) -> None:
        self.switch_to_slide(max(self.slide_index - 1, 0))

    def action_home(self) -> None:
        self.switch_to_slide(0)

    def switch_to_slide(self, index: int) -> None:
        curent_index = self.slide_index
        if index != curent_index:
            self.slide_index = index
            self.update_slide()

    def action_edit(self) -> None:
        if self.current_slide.path:
            with self.suspend():
                click.edit(filename=self.current_slide.path, editor=os.environ.get("EDITOR"))
            self.current_slide.reload()
        self.update_slide()

    @property
    def current_slide(self) -> "Slide":
        return self.slides[self.slide_index]

    def action_run(self) -> None:
        if self.current_slide.runnable:
            self.current_slide.run()
            self.update_slide()
            self.refresh()

    def update_slide(self):
        try:
            container_widget = self.query_one("#content", VerticalScroll)
            content_widget = self.slides[self.slide_index].render(app=self)
            container_widget.remove_children()
            container_widget.mount(content_widget)
            Path(".current_slide").write_text(str(self.slide_index))
        except QueryError:
            pass


@dataclass()
class Slide(ABC):
    path: Optional[str | Path] = field(default=None, kw_only=True)
    source: Optional[str] = ""
    runnable: ClassVar[bool] = False

    def __post_init__(self):
        self._load()

    def _load(self):
        if self.path:
            try:
                self.source = Path(self.path).read_text(encoding="utf-8")
            except FileNotFoundError:
                self.source = f"File not found: {self.path}."        

    def reload(self):
        self._load()

    @abstractmethod
    def render(self, app: App) -> Widget: ...

    def is_runnable(self) -> bool:
        return False

    def run(self) -> None:
        pass


@dataclass
class CodeSlide(Slide):
    """Slide with runnable code from external file or string."""

    language: str = "python"
    mode: Literal["code", "output"] = "code"
    requires_alt_screen: bool = False
    runnable: ClassVar[bool] = True
    wait_for_key: bool = True
    title: Optional[str] = None
    is_title_markdown: bool = False

    def render(self, app) -> Widget:
        match self.mode:
            case "code":
                return self._render_code()
            case "output":
                if self.requires_alt_screen:
                    self._exec_in_alternate_screen(app)
                    return self._render_code()
                return self._render_output(app=app)

    def _render_code(self) -> Markdown:
        code = "\n".join(
            " " + line.rstrip()
            for line in self.source.splitlines()
            if "# HIDE" not in line
        )
        if self.title:
            if self.is_title_markdown:
                return Markdown(self.title + f"\n\n```{self.language}\n{code}\n```")
            return Markdown(
                f"## {self.title}\n\n```{self.language}\n{code}\n```"
            )
        return Markdown(f"```{self.language}\n{code}\n```")

    def _render_output(self, app) -> Widget:
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        try:
            match self.language:
                case "python":
                    with redirect_stdout(f):
                        import plotext as plt

                        plt.plotsize(width=50, height=15)
                        self._exec(app=app)
                    output = f.getvalue()
                case "shell":
                    import subprocess
                    output = subprocess.check_output(self.source, shell=True).decode("utf-8")
        except Exception as ex:
            output = f"Error: {ex}"
        else:
            output = "\n".join(
                " " + line.rstrip() for line in output.splitlines()
            )
        output_widget = Static(Text.from_ansi(output))
        if self.title:
            if self.is_title_markdown:
                return Container(Markdown(self.title), output_widget)
            return Container(Markdown(f"## {self.title}"), output_widget)
        return output_widget

    def _exec(self, app: App) -> None:
        match self.language:
            case "python":
                exec(
                    self.source,
                    globals=globals()
                    | {
                        "WIDTH": app.size.width - 4,
                        "HEIGHT": app.size.height - 2,
                    },
                )
                import plotext as plt

                plt.clear_figure()
            case "shell":
                import os

                os.system(self.source)

    def run(self):
        self.mode = "output" if self.mode == "code" else "code"

    def _exec_in_alternate_screen(self, app):
        with app.suspend():
            console = Console()
            console.clear()
            self._exec(app)
            if self.wait_for_key:
                self._wait_for_key()
            self.mode = "code"
            console.clear()

    def _wait_for_key(self):
        rich.print("[bold]Press any key to continue...[/bold]")
        match sys.platform:
            case "win32":
                import msvcrt
                msvcrt.getch()
            case "linux" | "darwin":
                # Test this works on mac
                import tty
                import termios

                old_settings = termios.tcgetattr(sys.stdin)
                tty.setcbreak(sys.stdin.fileno())
                try:
                    os.read(sys.stdin.fileno(), 3).decode()
                finally:
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)



class MarkdownSlide(Slide):
    """Markdown slide with source from external file or string."""
    def render(self, app: App) -> Markdown:
        return Markdown(dedent(self.source))


@dataclass
class FuncSlide(Slide):
    """Any slide created from a function."""
    f: Callable[[App], Markdown | Text | str] = field(kw_only=True)
    source = ""  # ignored
    path = None  # ignored

    def render(self, app: App):
        rendered = self.f(app)
        if isinstance(rendered, Widget):
            return rendered
        elif isinstance(rendered, str):
            return Markdown(dedent(rendered))
        elif isinstance(rendered, (Text, Panel)):
            return Static(rendered)


def dyn_md(f: Callable[[App], Any]) -> FuncSlide:
    """Decorator to create a markdown slide from a function."""
    return FuncSlide(f=f)


def md(path: Optional[str | Path] = None, *, source: Optional[str] = None, **kwargs) -> MarkdownSlide:
    """Helper function to create a Markdown slide."""
    return MarkdownSlide(path=path, source=source, **kwargs)


def py(path: Optional[str | Path] = None, *, source: Optional[str] = None, **kwargs) -> CodeSlide:
    """Helper function to create a Python code slide."""
    return CodeSlide(path=path, source=source, language="python", **kwargs)


def sh(cmd, **kwargs) -> CodeSlide:
    """Helper function to create a shell command slide."""
    kwargs = {
        "language": "shell",
        **kwargs,
    }
    return CodeSlide(source=cmd, **kwargs)