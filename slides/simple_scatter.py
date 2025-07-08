import polars as pl
import numpy as np

cities = pl.read_parquet("data/cities.parquet")
# HIDE_ABOVE
cities = cities.filter(country="Czechia").sort("population", descending=True)

min_lat, max_lat = int(cities["lat"].min()), int(cities["lat"].max()) + 1
min_lon, max_lon = int(cities["lng"].min()), int(cities["lng"].max()) + 1
plotting_area = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

for data in cities.iter_rows(named=True):
    lat, lon = data["lat"], data["lng"]
    x = int((lon - min_lon) / (max_lon - min_lon) * WIDTH)
    y = int((max_lat - lat) / (max_lat - min_lat) * HEIGHT)
    name = data["city"]
    plotting_area[y][x] = name[0]

for row in plotting_area:
    print("".join(row))
