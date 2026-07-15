HEIGHT -= 2
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
    (255, 128, 0),
    (255, 0, 0),
    (255, 0, 128),
    (255, 0, 255),
    (255, 255, 255),
]
styles = [f"rgb({c[0]},{c[1]},{c[2]})" for c in colours_rgb]

scale = HEIGHT / array_levels.shape[1]
for i in range(HEIGHT):
    y = int(np.round(i / scale))
    for j in range(int(array_levels.shape[0] * scale * 2)):
        x = np.clip(int(np.round(j / (scale * 2))), 0, array_levels.shape[0] - 1)
        level = array_levels[y, x]
        if np.isnan(level):
            console.print(" ", end="")
        else:
            style = styles[int(np.clip(level, 0, len(styles) - 1))]
            console.print("█", style=style, end="")
    console.print()
