from abc import ABC, abstractmethod
from pathlib import Path
from textwrap import dedent
from dataclasses import dataclass, field
import subprocess
from typing import Optional, ClassVar, Literal, Callable

from rich.text import Text
from rich.console import Console
from textual.app import App
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import Markdown, Static
from rich.panel import Panel

from typing import Any

from clippt.utils import wait_for_key


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

    language: Literal["shell", "python"] = "python"
    mode: Literal["code", "output"] = "code"
    alt_screen: bool = False
    runnable: ClassVar[bool] = True
    wait_for_key: bool = True
    title: Optional[str] = None
    is_title_markdown: bool = False

    _output: Optional[str] = None

    def _load(self):
        self._output = None
        super()._load()

    def render(self, app) -> Widget:
        match self.mode:
            case "code":
                return self._render_code()
            case "output":
                if self.alt_screen:
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

        try:
            match self.language:
                case "python":
                    f = io.StringIO()
                    with redirect_stdout(f):
                        import plotext as plt

                        plt.plotsize(width=50, height=15)
                        self._exec(app=app)
                        output = f.getvalue()
                case "shell":
                    if not self._output:
                        with app.suspend():
                            p = subprocess.run(self.source, shell=True, capture_output=True, text=True, encoding="utf-8")
                            self._output = p.stdout
                    output = self._output
        except Exception as ex:
            output = f"Error: {ex}"
        else:
            output = "\n".join(
                " " + line.rstrip() for line in output.splitlines()
            )
        output_widget = Static(Text.from_ansi(output + "\n"))
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
                wait_for_key()
            self.mode = "code"
            console.clear()


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

    def render(self, app: App) -> Widget:
        rendered = self.f(app)
        if isinstance(rendered, Widget):
            return rendered
        elif isinstance(rendered, str):
            return Markdown(dedent(rendered))
        elif isinstance(rendered, (Text, Panel)):
            return Static(rendered)
        else:
            raise NotImplementedError()


def dyn_md(f: Callable[[App], Any]) -> FuncSlide:
    """Decorator to create a markdown slide from a function."""
    return FuncSlide(f=f)


def md(source: str, **kwargs) -> MarkdownSlide:
    """Helper function to create a simple Markdown slide."""
    return MarkdownSlide(path=None, source=source, **kwargs)


def py(source: str, **kwargs) -> CodeSlide:
    """Helper function to create a simple Python code slide."""
    return CodeSlide(path=None, source=source, language="python", **kwargs)


def sh(cmd, **kwargs) -> CodeSlide:
    """Helper function to create a shell command slide."""
    kwargs = {
        "language": "shell",
        **kwargs,
    }
    return CodeSlide(source=cmd, **kwargs)


def load(path: str | Path, **kwargs) -> Slide:
    """Load a slide from an external file."""
    path = Path(path)
    match path.suffix:
        case ".py":
            return CodeSlide(path=path, language="python", **kwargs)
        case ".md":
            return MarkdownSlide(path=path, **kwargs)
        case _:
            return MarkdownSlide(source=f"Unknown file type: {path}")
