import polars as pl  # HIDE

weather = pl.read_parquet("data/weather.parquet")
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
fig.width = 58  # WIDTH - 5   # HIDE
fig.height = 15  # HEIGHT     # HIDE

fig.histogram(
    daily["min_temp"],
    bins=50,
    lc="blue"
)

print("Minimum daily temperatures\n")
print(fig.show())
