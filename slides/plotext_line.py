import polars as pl  # HIDE

weather = pl.read_parquet("data/weather.parquet")
yearly = weather.group_by(
    pl.col("time").dt.year().alias("year"),
    maintain_order=True
).agg(
    min_temp=pl.col("temp").min(),
    max_temp=pl.col("temp").max(),
).filter(pl.col("year").is_between(1990, 2023))
# HIDE_ABOVE
import plotext as plt

plt.plotsize(WIDTH, HEIGHT)

plt.title("Yearly temperature")
plt.plot(yearly["year"], yearly["min_temp"], color="blue", label="min. temp")
plt.plot(yearly["year"], yearly["max_temp"], color="red", label="max. temp")
plt.show()
