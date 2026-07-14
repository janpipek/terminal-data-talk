import polars as pl  # HIDE

weather = pl.read_parquet("data/krakow-meteostat.parquet")
daily = weather.group_by_dynamic(
    "time",
    every="1d"
).agg(
    min_temp=pl.col("temp").min(),
    max_temp=pl.col("temp").max(),
    total_precipitation=pl.col("prcp").sum(),
).filter(pl.col("time").dt.year() >= 1990)
# HIDE_ABOVE
import plotille

fig = plotille.Figure()
fig.width = WIDTH - 20   # HIDE
fig.height = HEIGHT - 10  # HEIGHT     # HIDE

fig.histogram(
    daily["min_temp"],
    bins=50,
    lc="blue"
)

print("Minimum daily temperatures\n")
print(fig.show())
