import sys
from pathlib import Path

import polars as pl
from textual.app import App, ComposeResult
from textual_fastdatatable import DataTable
from textual_fastdatatable.backend import PolarsBackend


class DataApp(App):
    data: pl.DataFrame

    def __init__(self, data: pl.DataFrame, **kwargs):
        super().__init__(**kwargs)
        self.data = data

    def compose(self) -> ComposeResult:
        backend = PolarsBackend.from_dataframe(self.data)
        yield DataTable(backend=backend, zebra_stripes=True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Please, provide exactly one path.")
        sys.exit(-1)
    path = Path(sys.argv[1])
    method_candidate = f"read_{path.suffix[1:]}"
    if hasattr(pl, method_candidate):
        data = ...
