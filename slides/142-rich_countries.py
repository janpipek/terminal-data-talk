import polars as pl  # HIDE
from rich.console import Console  # HIDE
from rich.table import Table  # HIDE
df = pl.read_csv("data/countries.csv")  # HIDE
# HIDE
...
def show_table(df: pl.DataFrame):
    table = Table()
    for col in df.columns:
        table.add_column(col)
    for row in df.iter_rows():
        table.add_row(*(str(v) for v in row))
    console = Console()
    console.print(table)

countries = df.filter(region="Asia").sort("population", descending=True)
show_table(countries)
