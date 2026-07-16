def render_mandelbrot(
    *,
    center: tuple[float, float] = (0.0, 0.0),
    span: tuple[float, float] = (4.0, 2.0),
    cols: int,
    rows: int,
    char: str = "●",
) -> str:
    x_step = span[0] / (cols - 1)
    y_step = span[1] / (rows - 1)
    return "\n\n" + "\n".join(
        "    "
        + "".join(
            char
            if in_mandelbrot(
                complex(
                    center[0] + (x - cols / 2) * x_step,
                    center[1] + (y - rows / 2) * y_step,
                )
            )
            else " "
            for x in range(cols)
        )
        for y in range(rows)
    )


# HIDE_ABOVE
def in_mandelbrot(c: complex, *, iterations: int = 256) -> bool:
    """Check if a complex number is in the Mandelbrot set.

    This is a set in the complex plane which looks like this:

                       **
                    ********
                   *********
             **** ***********
     ***********************
             **** ***********
                   *********
                    ********
                       **

    :param iterations: Number of iterations to run the Mandelbrot algorithm
    """
    ...
    # HIDE_BELOW
    z = 0j
    for _ in range(iterations):
        z = z * z + c
        if abs(z) > 2:
            return False
    return True


# HIDE_BELOW
print(render_mandelbrot(cols=41, rows=12, char="*"))
