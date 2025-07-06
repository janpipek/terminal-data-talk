import polars as pl  # HIDE
from rich.console import Console  # HIDE
from rich.table import Table  # HIDE

pl.Config.set_tbl_rows(1000)  # HIDE


def show_table(df: pl.DataFrame):  # HIDE
    table = Table()  # HIDE
    for col in df.columns:  # HIDE
        table.add_column(col)  # HIDE
    for row in df.iter_rows():  # HIDE
        table.add_row(*(str(v) for v in row))  # HIDE
    console = Console()  # HIDE
    console.print(table)  # HIDE


# HIDE
cities = pl.read_parquet("data/cities.parquet")
# 47868 rows, 11 columns

# Don't run this!
show_table(cities)
