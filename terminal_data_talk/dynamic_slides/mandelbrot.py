import asyncio

from clippt.slides import Slide
from rich.text import Text
from textual.app import App
from textual.widget import Widget
from textualeffects.effects import effects
from textualeffects.widgets import EffectLabel

ITERATIONS = 400
X_SPAN = 3.0
X_CENTER = -0.5
# Terminal cells are ~2x taller than wide; double the y step to keep aspect.
CELL_ASPECT = 2.0
# Real delay between frames — TTE itself doesn't pace; ``asyncio.sleep(0)``
# in the upstream EffectLabel just yields to the event loop, so any effect
# rips by very fast. ~50ms/frame (~20 fps) is a comfortable ambient pace.
FRAME_DELAY = 1 / 60
# ColorShift has no native "loop forever", just a finite ``cycles`` count.
# Setting it absurdly high gives us hours of continuous animation per slide.
COLOR_CYCLES = 1_000_000


def in_mandelbrot(c: complex, *, iterations: int = ITERATIONS) -> bool:
    z = 0j
    for _ in range(iterations):
        z = z * z + c
        if abs(z) > 2:
            return False
    return True


def render(*, cols: int, rows: int) -> str:
    x_step = X_SPAN / cols
    y_step = x_step * CELL_ASPECT
    return "\n\n" + "\n".join(
        "    "
        + "".join(
            "●"
            if in_mandelbrot(
                complex(
                    X_CENTER + (x - cols / 2) * x_step,
                    (y - rows / 2) * y_step,
                )
            )
            else " "
            for x in range(cols)
        )
        for y in range(rows - 1)
    )


class PacedEffectLabel(EffectLabel):
    """EffectLabel that paces frames with a real delay.

    Upstream uses ``asyncio.sleep(0)`` per frame which only yields to the event
    loop, so animations finish in a blink. We swap in ``FRAME_DELAY`` for a
    cinematic pace.
    """

    async def run_effect(self) -> None:
        effect = effects[self.effect](self.text)
        for key, value in self.config.items():
            if hasattr(effect.effect_config, key):
                setattr(effect.effect_config, key, value)
        effect.terminal_config.canvas_width = self.width
        effect.terminal_config.canvas_height = self.height
        for frame in effect:
            self.text = frame
            self.update(Text.from_ansi(self.text))
            await asyncio.sleep(FRAME_DELAY)


class MandelbrotSlide(Slide):
    """Fills the slide content area with a Mandelbrot, animated by TTE's ColorShift.

    Subclasses ``Slide`` directly (not ``FuncSlide``) so we receive the exact
    cell dimensions of the content area — ``EffectLabel`` pins its width and
    height to the input text, so the art must be generated at the final size.
    """

    source: str = ""
    path: None = None

    def _render_impl(self, app: App, *, columns: int, rows: int) -> Widget:
        # EffectLabel adds 2 cells of styling padding to each dimension.
        art = render(cols=max(columns - 2, 20), rows=max(rows - 2, 10))
        return PacedEffectLabel(
            art,
            effect="ColorShift",
            config={"cycles": COLOR_CYCLES},
        )
