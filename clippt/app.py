import os
from pathlib import Path
from clippt.slides import Slide, load

import click
from textual.app import App, ComposeResult
from textual.containers import  VerticalScroll, Container
from textual.widgets import Footer
from textual.css.query import QueryError

from clippt.theming import my_theme, css_tweaks


class PresentationApp(App):
    """A Textual app for the presentation."""

    enable_footer: bool = True

    BINDINGS = [
        ("pageup", "prev_slide", "Previous"),
        ("pagedown", "next_slide", "Next"),
        (".", "run", "Run"),
        ("q", "quit", "Quit"),
        ("e", "edit", "Edit"),
        ("r", "reload", "Reload"),
        ("home", "home", "First slide"),
    ]

    CSS = css_tweaks

    slide_index: int = 0

    slides: list[Slide]

    document_title: str

    def __init__(self, *, slides: list[str | Path | Slide], title: str, **kwargs):
        self.slides = self._ensure_load_slides(slides)
        self.document_title = title
        super().__init__(**kwargs)

    def _ensure_load_slides(self, slides: list[Slide | str | Path]) -> list[Slide]:
        return [
            slide_or_path
            if isinstance(slide_or_path, Slide)
            else load(slide_or_path)
            for slide_or_path in slides
        ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        # yield Header(show_clock=True)
        yield Container(
            self.current_slide.render(app=self), id="content"  #, can_focus=False
        )
        if self.enable_footer:
            yield Footer(show_command_palette=False)

    def on_mount(self) -> None:
        """Hook called when the app is mounted."""
        self.register_theme(my_theme)
        self.theme = "my"

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
                click.edit(filename=[self.current_slide.path], editor=os.environ.get("EDITOR"))
            self.current_slide.reload()
        self.update_slide()

    def action_run(self) -> None:
        if self.current_slide.runnable:
            self.current_slide.run()
            self.update_slide()
            self.refresh()

    @property
    def current_slide(self) -> Slide:
        return self.slides[self.slide_index]

    def update_slide(self) -> None:
        try:
            container_widget = self.query_one("#content", Container)
            container_widget.remove_children()
            self.refresh()
            content_widget = self.slides[self.slide_index].render(app=self)
            container_widget.mount(content_widget)
            Path(".current_slide").write_text(str(self.slide_index))
        except QueryError:
            pass
