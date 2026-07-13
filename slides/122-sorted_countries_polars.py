import polars as pl

pl.Config.set_tbl_rows(1000)  # HIDE
pl.Config.set_tbl_width_chars(WIDTH)  # HIDE
df = pl.read_csv("data/countries.csv")
df = df.filter(region="Asia").sort("population", descending=True)
print(df)
pl.Config.restore_defaults()  # HIDE
