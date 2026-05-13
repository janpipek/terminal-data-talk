import shutil

from terminaltexteffects.effects.effect_burn import Burn

ITERATIONS = 40
# Classic Mandelbrot view centred on (-0.5, 0); width 3.0 in the complex plane.
X_SPAN = 3.0
X_CENTER = -0.5
# Terminal cells are ~2x taller than wide, so we double the y step to keep aspect.
CELL_ASPECT = 2.0


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
    return "\n".join(
        "".join(
            "*"
            if in_mandelbrot(
                complex(
                    X_CENTER + (x - cols / 2) * x_step,
                    (y - rows / 2) * y_step,
                )
            )
            else " "
            for x in range(cols)
        )
        for y in range(rows)
    )


cols, rows = shutil.get_terminal_size()
art = render(cols=cols, rows=rows - 1)

effect = Burn(art)
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)
