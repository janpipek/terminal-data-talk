import polars as pl

pl.Config.set_tbl_rows(-1)  # Do not limit
df = pl.read_parquet("data/cities.parquet")
print(df)
pl.Config.restore_defaults()  # HIDE
