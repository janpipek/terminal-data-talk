HEIGHT -= 3
# HIDE_ABOVE
import numpy as np
from rich.console import Console

console = Console()

elevation = np.load("./data/poland_elevation_512.npy")
levels = [0, 100, 200, 300, 500, 750, 1000, 1500, 2000, 3000]
array_levels = np.digitize(elevation, levels)

colours_rgb = [
    (0, 220, 128),
    (0, 255, 0),
    (128, 255, 0),
    (255, 255, 0),
    (255, 192, 0),
    (255, 80, 0),
    (255, 0, 0),
    (255, 0, 128),
    (255, 0, 255),
    # (255, 255, 255),
]
styles = [f"rgb({c[0]},{c[1]},{c[2]})" for c in colours_rgb]

scale_y = HEIGHT / array_levels.shape[1]
scale_x = scale_y * 2
indent = (WIDTH - int(np.round(scale_x * array_levels.shape[0]))) // 2

for i in range(HEIGHT):
    console.print(" " * indent, end="")
    y = int(np.round(i / scale_y))
    for j in range(int(array_levels.shape[0] * scale_x)):
        x = np.clip(int(np.round(j / scale_x)), 0, array_levels.shape[0] - 1)
        level = array_levels[y, x]
        try:
            style = styles[level]
            console.print("█", style=style, end="")
        except IndexError:
            console.print(" ", end="")
    console.print()
