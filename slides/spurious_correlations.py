from pathlib import Path

import plotext as plt
import polars as pl  # HIDE

plt.clear_figure()  # HIDE
data = pl.read_csv(
    Path(__file__).parent.parent / "slides" / "spurious_correlations.csv"
)
plt.plot(
    data["Year"], data["Fuel Used"], label="Jet fuel used in Czechia", yside="left"
)
plt.plot_size(WIDTH, HEIGHT)
plt.plot(
    data["Year"],
    data["Everest Climbs"],
    label="Total Number of Successful Mount Everest Climbs",
    yside="right",
)
plt.xticks([1995, 2000, 2005, 2010])
plt.yticks([3, 4, 5, 6, 7, 8], yside="left")
plt.yticks([100, 200, 300, 400, 500, 600], yside="right")
plt.xlabel("Year")
plt.ylabel("Million Barrels/day", yside="left")
plt.ylabel("Climbers", yside="right")
plt.canvas_color("default")
plt.axes_color("default")
plt.show()
