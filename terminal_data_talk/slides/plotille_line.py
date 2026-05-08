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
... # Similar with max. temp
fig.plot(  # HIDE
    yearly["year"], # HIDE
    yearly["max_temp"], # HIDE
    lc="red", # HIDE
    marker="o", # HIDE
     label="Max. temperature",  # HIDE
) # HIDE
print("Yearly temperatures\n")
print(fig.show(legend=True))
