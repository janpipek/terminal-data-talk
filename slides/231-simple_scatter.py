import polars as pl
import numpy as np

cities = pl.read_parquet("data/cities.parquet")
HEIGHT -= 2
# HIDE_ABOVE
cities = cities.filter(pl.col("population") > 20_000, country="Poland").sort("population", descending=False)

min_lat, max_lat = int(cities["lat"].min()), int(cities["lat"].max()) + 1
min_lon, max_lon = int(cities["lng"].min()), int(cities["lng"].max()) + 1
plotting_area = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
scale = (max_lat - min_lat) / HEIGHT

for data in cities.iter_rows(named=True):
    lat, lon = data["lat"], data["lng"]
    x = int((lon - min_lon) / scale * 2)
    y = int((max_lat - lat) / scale)
    name = data["city"]
    plotting_area[y][x] = name[0]

for row in plotting_area:
    print("".join(row))
