import os
import sys
if __name__ != "__main__":
    os.system(sys.executable + " " + "slides/data_table.py data/cities.parquet")

# HIDE_ABOVE
import polars as pl
from textual.app import App, ComposeResult
from textual.widgets import DataTable

class DataApp(App):
    def compose(self) -> ComposeResult:
        dt = DataTable()
        dt.add_columns("a", "b", "c")
        dt.add_row(["1, 2, 3"])
        yield dt

if __name__ == "__main__":
    app = DataApp()
    app.run()
