import polars as pl
from textual import on
from textual.app import App
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Label, ListItem, ListView, Markdown, Static
from textual_plotext import PlotextPlot

from clippt.slides import slide


class YearInfoWidget(Container):
    def compose(self):
        """Create child widgets of a stopwatch."""
        yield Markdown("## Overall stats", id="overall_stats")
        yield Markdown("**Total precipitation**: N/A", id="overall_prec")

    def update(self, year_data: pl.DataFrame):
        overall_prec = int(year_data["prcp"].sum())
        prec: Markdown = self.get_child_by_id("overall_prec", Markdown)
        prec.update(f"**Total precipitation**: {overall_prec} mm")
        # self.refresh()


class WeatherDashboard(Container):
    def __init__(self, data, **kwargs) -> None:
        super().__init__(**kwargs)
        self.data = data
        self.available_years: list[int] = sorted(
            self.data.select(year=pl.col("time").dt.year())["year"].unique()
        )[::-1]

    def compose(self):
        """Create child widgets of a stopwatch."""
        yield Markdown("# Prague Weather Dashboard")
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
        self._update_monthly_plot()
        self._update_year_info()

    @on(ListView.Selected, "#year_list")
    def _year_selected(self):
        list_view = self.get_widget_by_id("year_list", ListView)
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

    def _update_monthly_plot(self):
        widget = self.get_widget_by_id("monthly_plot", PlotextPlot)
        if widget:
            data = self.data.filter(pl.col("time").dt.year() == self.year)
            monthly = (
                data.group_by_dynamic("time", every="1mo")
                .agg(
                    pl.col("temp").min().alias("min_temp"),
                    pl.col("temp").mean().alias("mean_temp"),
                    pl.col("temp").max().alias("max_temp"),
                )
                .with_columns(month=pl.col("time").dt.strftime("%d/%m/%Y"))
            )

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
            widget.refresh()

    def _update_year_info(self):
        widget = self.get_widget_by_id("year_info", YearInfoWidget)
        data = self.data.filter(pl.col("time").dt.year() == self.year)
        widget.update(data)


@slide
def weather_dashboard(app: App) -> WeatherDashboard:
    data = pl.read_parquet("data/weather.parquet")
    data = data.filter(pl.col("time").dt.year() >= 2004)
    return WeatherDashboard(data=data)
