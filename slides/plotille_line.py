import polars as pl  # HIDE
import plotille

weather = pl.read_parquet("data/weather.parquet")
yearly = weather.group_by(
    pl.col("time").dt.year().alias("year"), maintain_order=True
).agg(
    min_temp=pl.col("temp").min(), max_temp=pl.col("temp").max(),
).filter(pl.col("year") >= 1990)

fig = plotille.Figure()
fig.width = 60   # HIDE
fig.height = 20    # HIDE
fig.plot(
    yearly["year"],
    yearly["min_temp"],
    lc="blue",
    marker="o",
    label="Min. temperature",
)
fig.plot(
    yearly["year"],
    yearly["max_temp"],
    lc="red",
    marker="o",
    label="Max. temperature",
)
print("Yearly temperatures\n")
print(fig.show(legend=True))
