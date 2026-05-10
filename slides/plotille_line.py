import os
os.environ["FORCE_COLOR"] = "1"

import polars as pl
# HIDE_ABOVE
import plotille

weather = pl.read_parquet("data/weather.parquet")
yearly = weather.group_by(
    pl.col("time").dt.year().alias("year"), maintain_order=True
).agg(
    min_temp=pl.col("temp").min(), max_temp=pl.col("temp").max(), mean_temp=pl.col("temp").mean()
).filter(pl.col("year") >= 1990)

fig = plotille.Figure()
fig.width = WIDTH - 17 # WIDTH   # HIDE
fig.height = HEIGHT - 15    # HIDE
fig.plot(
    yearly["year"],
    yearly["min_temp"],
    lc="blue",
    marker="o",
    label="Min. temperature",
)
# ... Similar with max. temp
fig.plot(  # HIDE
    yearly["year"], # HIDE
    yearly["max_temp"], # HIDE
    lc="red", # HIDE
    marker="o", # HIDE
    label="Max. temperature",  # HIDE
) # HIDE
# ... and mean temp
fig.plot(  # HIDE
    yearly["year"], # HIDE
    yearly["mean_temp"], # HIDE
    lc="green", # HIDE
    marker="o", # HIDE
    label="Mean temperature",  # HIDE
) # HIDE

print("Yearly temperatures\n")
print(fig.show(legend=True))
# HIDE_BELOW
del os.environ["FORCE_COLOR"]
