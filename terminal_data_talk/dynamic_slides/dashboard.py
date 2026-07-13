from functools import lru_cache

import polars as pl
from clippt.slides import FuncSlide
from textual import on
from textual.app import App
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Label, ListItem, ListView, Markdown, Static
from textual_plotext import PlotextPlot


def slide(f):
    return FuncSlide(f=f)


class YearInfoWidget(Container):
    def compose(self):
        """Create child widgets of a stopwatch."""
        yield Markdown("## Overall stats", id="header")
        yield Markdown("N/A", id="table")

    def update(self, *, year_data: pl.DataFrame, year: int):
        overall_prec = int(year_data["prcp"].sum())
        min_temp = float(year_data["temp"].min())
        max_temp = float(year_data["temp"].max())
        avg_temp = float(year_data["temp"].mean())
        try:
            year_widget: Markdown = self.get_child_by_id("header", Markdown)
            year_widget.update(f"## Overall stats for {year}")

            prec: Markdown = self.get_child_by_id("table", Markdown)
            text = (
                "| Metric              | Value           |\n"
                "|---------------------|----------------|\n"
                f"| Total precipitation | {overall_prec} mm |\n"
                f"| Min temperature     | {min_temp}°C      |\n"
                f"| Max temperature     | {max_temp}°C      |\n"
                # f"| Avg temperature     | {avg_temp:.1f}°C      |"
            )
            prec.update(text)
        except:
            pass


class WeatherDashboard(Container):
    ylims = (-20, 40)
    station: str

    def __init__(self, data, *, station=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.data = data
        self.station = str(station or "Unknown")
        self.available_years: list[int] = sorted(
            self.data.select(year=pl.col("time").dt.year())["year"].unique()
        )[::-1]

    def compose(self):
        yield Markdown(f"# Weather Dashboard: {self.station}")
        with Horizontal():
            with Vertical():
                yield Static("[blue]Select year[/blue]")
                yield self.create_year_list()
                yield self.create_year_info()
            yield PlotextPlot(id="monthly_plot")

    def create_year_info(self):
        container = YearInfoWidget(id="year_info")
        return container

    def on_mount(self):
        self.year = self.available_years[0]
        # Use call_after_refresh to ensure widgets are fully mounted
        self.call_after_refresh(self._update_monthly_plot)
        self.call_after_refresh(self._update_year_info)

    @on(ListView.Selected, "#year_list")
    def _year_selected(self):
        list_view = self.query_one("#year_list", ListView)
        self.year = self.available_years[list_view.index]
        self._update_monthly_plot()
        self._update_year_info()

    def create_year_list(self):
        list_view = ListView(
            *[ListItem(Label(str(year))) for year in self.available_years],
            id="year_list",
        )
        list_view.can_focus = False
        return list_view

    @lru_cache
    def compute_monthly_summary(self, year: int) -> pl.DataFrame:
        data = self.data.filter(pl.col("time").dt.year() == self.year)
        return (
            data.group_by_dynamic("time", every="1mo")
            .agg(
                pl.col("temp").min().alias("min_temp"),
                pl.col("temp").mean().alias("mean_temp"),
                pl.col("temp").max().alias("max_temp"),
            )
            .with_columns(month=pl.col("time").dt.strftime("%d/%m/%Y"))
        )

    def _update_monthly_plot(self):
        try:
            widget = self.query_one("#monthly_plot", PlotextPlot)
        except:
            return
        if widget:
            monthly = self.compute_monthly_summary(self.year)

            widget.plt.clear_figure()
            widget.plt.plot(
                monthly["month"], monthly["min_temp"], marker="·", color="blue"
            )
            widget.plt.scatter(
                monthly["month"], monthly["min_temp"], marker="o", color="blue"
            )
            widget.plt.plot(
                monthly["month"], monthly["max_temp"], marker="·", color="red"
            )
            widget.plt.scatter(
                monthly["month"], monthly["max_temp"], marker="o", color="red"
            )
            widget.plt.plot(
                monthly["month"], monthly["mean_temp"], marker="·", color="gray"
            )
            widget.plt.scatter(
                monthly["month"], monthly["mean_temp"], marker="∅︎", color="gray"
            )
            widget.plt.title(f"Monthly temperatures of {self.year}")
            widget.plt.ylim(*self.ylims)
            widget.plt.xlabel("Month")
            widget.refresh()

    def _update_year_info(self):
        try:
            widget = self.query_one("#year_info", YearInfoWidget)
        except:
            return
        data = self.data.filter(pl.col("time").dt.year() == self.year)
        widget.update(year=self.year, year_data=data)


@slide
def weather_dashboard(app: App) -> WeatherDashboard:
    data = pl.read_parquet("data/plzen-meteostat.parquet")
    # data = data.filter(pl.col("time").dt.year() >= 2004)
    return WeatherDashboard(data=data, station="Plzeň-Líně")
