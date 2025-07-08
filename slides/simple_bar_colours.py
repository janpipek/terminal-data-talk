import polars as pl
from rich.console import Console

# HIDE_ABOVE
countries = (
    pl.read_csv("data/countries.csv")
    .filter(region="Asia")
    .sort("population", descending=True)
    .select("country", "population")
)
countries = countries.head(15)  # HIDE_ABOVE
data = {country: population for country, population in countries.iter_rows()}

# Some measurements
MAX_BAR_WIDTH = 40  # HIDE
label_width = max(len(label) for label in data)
max_value = max(data.values())

# Draw line of various widths
even = False

console = Console(color_system="truecolor")

for label, value in data.items():
    n_chars = int(value / max_value * WIDTH / 2)
    if even:
        console.print(f"  [bold][green]{label:{label_width}}[/bold][/green] [white on #ff8080]{' ' * n_chars}[/] {value}")
    else:
        console.print(f"  [bold][green]{label:{label_width}}[/bold][/green] [white on #ffc0c0]{' ' * n_chars}[/] {value}")
    even = not even
