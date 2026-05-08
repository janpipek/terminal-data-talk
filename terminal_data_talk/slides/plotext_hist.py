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
import plotext as plt

plt.plotsize(WIDTH, HEIGHT)

bins = 60
plt.hist(daily["min_temp"], bins, color="blue", label = "min. temp")
plt.hist(daily["max_temp"], bins, color="red", label = "max. temp")

plt.title("Histogram Plot")
plt.show()
