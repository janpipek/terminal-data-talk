"""Animated EuroPython 2026 logo rendered as character art.

The logo is redrawn as pure terminal art (no bitmap): a navy disc with the
twelve EU stars slowly orbiting a pixel-art Python emblem, and block-letter
"EURO PYTHON 2026" underneath. Rebuilding the whole frame each tick is cheap
(a few thousand cells) and keeps the renderer a pure function of
``(columns, rows, angle)``, which makes it easy to preview outside the app.
"""

import math

from clippt.slides import Slide
from rich.style import Style
from rich.text import Text
from textual.app import App
from textual.widget import Widget
from textual.widgets import Static

NAVY = "#12233f"
STAR_GOLD = "#ffd343"
SNAKE_BLUE = "#3776ab"
SNAKE_YELLOW = "#ffd43b"
# The original lettering is white with a dark outline — invisible on the
# light presentation theme — so we reuse the disc navy for EURO/PYTHON.
LETTER_COLOR = NAVY
RED_GRADIENT = ("#e8484e", "#8f0f1f")  # top and bottom of "2026"

STAR_COUNT = 12
STAR_RING_RATIO = 0.82  # star ring radius relative to the disc radius
ROTATION_PERIOD = 15.0  # seconds per full revolution
FPS = 10
# Terminal cells are ~2x taller than wide; stretch x by this to get a circle.
CELL_ASPECT = 2.0
# Disc y-radius bounds: the cap keeps the circle modest on tall screens,
# the floor keeps it recognizable on short ones (e.g. a 25-row projector).
MAX_DISC_RADIUS = 12
MIN_DISC_RADIUS = 5

# Pixel-art Python emblem: B/Y = blue/yellow snake, o = white eye.
# Each logical pixel becomes two cells wide to compensate for cell aspect.
PYTHON_ART = [
    "...BBBBBB...",
    "...BoBBBB...",
    "...BBBBBB...",
    ".BBBBBBBBYY.",
    ".BBBBBBBBYY.",
    ".BBBBBBBBYY.",
    ".BBYYYYYYYY.",
    ".BBYYYYYYYY.",
    ".BBYYYYYYYY.",
    "...YYYYYY...",
    "...YYYYoY...",
    "...YYYYYY...",
]
# Mid-size snake for ry 7-8 discs: big enough to keep the emblem shape,
# small enough (9x9, centred on the disc) to stay clear of the star ring.
PYTHON_ART_MEDIUM = [
    "..BBBBB..",
    "..BoBBB..",
    "BBBBBBBYY",
    "BBBBBBBYY",
    "BBBBBYYYY",
    "BBYYYYYYY",
    "BBYYYYYYY",
    "..YYYoY..",
    "..YYYYY..",
]
# Reduced snake for small discs where the full art would overlap the stars.
PYTHON_ART_SMALL = [
    "..BBBB..",
    "..BoBB..",
    "BBBBBBYY",
    "BBYYYYYY",
    "..YYoY..",
    "..YYYY..",
]
ART_COLORS = {"B": SNAKE_BLUE, "Y": SNAKE_YELLOW, "o": "#ffffff"}

# 5x5 block glyphs for the letters the logo needs.
FONT = {
    "E": ["#####", "#....", "####.", "#....", "#####"],
    "U": ["#...#", "#...#", "#...#", "#...#", ".###."],
    "R": ["####.", "#...#", "####.", "#..#.", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "####.", "#....", "#...."],
    "Y": ["#...#", ".#.#.", "..#..", "..#..", "..#.."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#.."],
    "H": ["#...#", "#...#", "#####", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#"],
    "2": [".###.", "#...#", "..##.", ".#...", "#####"],
    "0": [".###.", "#..##", "#.#.#", "##..#", ".###."],
    "6": [".###.", "#....", "####.", "#...#", ".###."],
    " ": ["..", "..", "..", "..", ".."],
}


class EuroPythonLogoSlide(Slide):
    """Full-screen animated EuroPython 2026 logo.

    Subclasses ``Slide`` directly (like ``MandelbrotSlide``) to receive the
    exact cell dimensions of the content area, so the art can be sized to
    fill the screen.
    """

    source: str = ""
    path: None = None

    def _render_impl(self, app: App, *, columns: int, rows: int) -> Widget:
        return RotatingLogoWidget(columns=columns, rows=rows)


class RotatingLogoWidget(Static):
    """Static widget that advances the star-ring rotation on a timer."""

    def __init__(self, *, columns: int, rows: int) -> None:
        super().__init__()
        self._columns = columns
        self._rows = rows
        self._angle = 0.0

    def on_mount(self) -> None:
        self._tick()
        self.set_interval(1 / FPS, self._tick)

    def _tick(self) -> None:
        self._angle += 2 * math.pi / (ROTATION_PERIOD * FPS)
        self.update(
            render_frame(columns=self._columns, rows=self._rows, angle=self._angle)
        )


def render_frame(*, columns: int, rows: int, angle: float) -> Text:
    """Render one frame of the logo as rich Text.

    Pure function so frames can be previewed outside the Textual app.
    """
    grid = _Grid(columns=columns, rows=rows)

    lettering = _render_lettering()
    text_height = len(lettering)

    # Vertical layout: disc on top, lettering below, everything centred.
    disc_ry = (rows - text_height - 2) // 2
    # Disc width is 2*rx + 1 = 2 * CELL_ASPECT * ry + 1 cells.
    disc_ry = min(disc_ry, int((columns - 3) / (2 * CELL_ASPECT)), MAX_DISC_RADIUS)
    disc_ry = max(disc_ry, MIN_DISC_RADIUS)
    disc_ry = 7
    # Sacrifice the disc-to-lettering gap rather than clip the year's bottom.
    gap = 1 if (2 * disc_ry + 2) + text_height <= rows else 0
    total_height = (2 * disc_ry + 1) + gap + text_height
    top = max((rows - total_height) // 2, 0)
    center_x = columns // 2
    center_y = top + disc_ry

    _draw_disc(grid, cx=center_x, cy=center_y, ry=disc_ry)
    _draw_python(grid, cx=center_x, cy=center_y, ry=disc_ry)
    _draw_stars(grid, cx=center_x, cy=center_y, ry=disc_ry, angle=angle)

    for i, line in enumerate(lettering):
        y = top + 2 * disc_ry + 1 + gap + i
        x = center_x - sum(len(chars) for chars, _ in line) // 2
        for chars, style in line:
            for char in chars:
                grid.put(x, y, char, style)
                x += 1

    return grid.to_text()


class _Grid:
    """Cell buffer of (char, style) pairs that compresses into rich Text."""

    def __init__(self, *, columns: int, rows: int) -> None:
        self.columns = columns
        self.rows = rows
        self.cells: list[list[tuple[str, Style | None]]] = [
            [(" ", None)] * columns for _ in range(rows)
        ]

    def put(self, x: int, y: int, char: str, style: Style | None) -> None:
        if 0 <= x < self.columns and 0 <= y < self.rows:
            self.cells[y][x] = (char, style)

    def to_text(self) -> Text:
        text = Text()
        for y, row in enumerate(self.cells):
            if y:
                text.append("\n")
            run_start = 0
            for x in range(1, self.columns + 1):
                if x == self.columns or row[x][1] is not row[run_start][1]:
                    chars = "".join(cell[0] for cell in row[run_start:x])
                    text.append(chars, style=row[run_start][1])
                    run_start = x
        return text


def _draw_disc(grid: _Grid, *, cx: int, cy: int, ry: int) -> None:
    style = Style(bgcolor=NAVY)
    for dy in range(-ry, ry + 1):
        # Per-row half-width; rows narrower than one cell (the poles) are
        # skipped so the disc has no single-cell nubs sticking out.
        half_width = CELL_ASPECT * math.sqrt(ry**2 - dy**2)
        if half_width < 1:
            continue
        for dx in range(-round(half_width), round(half_width) + 1):
            grid.put(cx + dx, cy + dy, " ", style)


def _draw_stars(grid: _Grid, *, cx: int, cy: int, ry: int, angle: float) -> None:
    style = Style(color=STAR_GOLD, bgcolor=NAVY, bold=True)
    ring = ry * STAR_RING_RATIO
    for i in range(STAR_COUNT):
        theta = angle + i * 2 * math.pi / STAR_COUNT
        x = cx + round(math.cos(theta) * ring * CELL_ASPECT)
        y = cy + round(math.sin(theta) * ring)
        grid.put(x, y, "★", style)


def _draw_python(grid: _Grid, *, cx: int, cy: int, ry: int) -> None:
    styles = {
        key: Style(color=color, bgcolor=NAVY) for key, color in ART_COLORS.items()
    }
    # The full snake needs a disc of radius >= 8 to stay clear of the stars;
    # the medium one fits ry == 7, anything smaller gets the reduced snake.
    if ry > 8:
        art = PYTHON_ART
    elif ry >= 7:
        art = PYTHON_ART_MEDIUM
    else:
        art = PYTHON_ART_SMALL
    top = cy - len(art) // 2
    left = cx - len(art[0])  # each logical pixel is two cells wide
    for dy, line in enumerate(art):
        for dx, key in enumerate(line):
            if key in styles:
                grid.put(left + 2 * dx, top + dy, "█", styles[key])
                grid.put(left + 2 * dx + 1, top + dy, "█", styles[key])


def _render_lettering() -> list[list[tuple[str, Style]]]:
    """Build the lettering lines as styled runs."""
    letter_style = Style(color=LETTER_COLOR, bold=True)
    lines = _render_word("EURO PYTHON", style=letter_style)
    lines += [[]]
    for row in range(5):
        color = _blend(RED_GRADIENT[0], RED_GRADIENT[1], row / 4)
        (line,) = _render_word("2026", style=Style(color=color, bold=True), rows=[row])
        lines.append(line)
    return lines


def _render_word(
    word: str, *, style: Style, rows: list[int] | None = None
) -> list[list[tuple[str, Style]]]:
    lines = []
    for row in rows if rows is not None else range(5):
        chars = " ".join(FONT[letter][row] for letter in word)
        lines.append([(chars.replace("#", "█").replace(".", " "), style)])
    return lines


def _blend(start: str, end: str, fraction: float) -> str:
    channels = (
        round(
            int(start[i : i + 2], 16) * (1 - fraction)
            + int(end[i : i + 2], 16) * fraction
        )
        for i in (1, 3, 5)
    )
    return "#" + "".join(f"{c:02x}" for c in channels)
