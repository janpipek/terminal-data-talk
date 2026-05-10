import os
import sys
if __name__ != "__main__":
    os.system(sys.executable + " " + "slides/data_viewer.py data/cities.parquet")

# HIDE_ABOVE
from pathlib import Path
import polars as pl
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from textual_fastdatatable import DataTable
from textual_fastdatatable.backend import PolarsBackend

class DataApp(App):
    data: pl.DataFrame

    BINDINGS = [("q", "quit", "Quit"),]

    def __init__(self, data: pl.DataFrame, **kwargs):
        super().__init__(**kwargs)
        self.data = data

    def compose(self) -> ComposeResult:
        backend = PolarsBackend.from_dataframe(self.data)
        yield Header()
        yield DataTable(backend=backend, zebra_stripes=True)
        yield Footer()

def browse(path: Path):
    # Magic read
    method_candidate = f"read_{path.suffix[1:]}"
    if method := getattr(pl, method_candidate):
        data = method(path)
    else:
        raise ValueError(f"Unknown file type: {path}")
    app = DataApp(data)
    app.title = f"{path} {data.shape}"
    app.run()

if __name__ == "__main__":
    browse(Path(sys.argv[1]))
