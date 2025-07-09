import polars as pl
import random

print()

countries = (
    pl.read_csv("data/countries.csv")
    .filter(region="Asia")
    .sort("population", descending=True)
    .select("country", "population")
)
# HIDE_ABOVE
countries = countries.head(15)
data = {country: population for country, population in countries.iter_rows()}

# Some measurements
MAX_BAR_WIDTH = 40  # HIDE
label_width = max(len(label) for label in data)
max_value = max(data.values())

# Draw line of various widths
for label, value in data.items():
    n_chars = max(int(value / max_value * WIDTH / 4), 1)
    chars = "".join([
        random.choice("🤕👶👨👱🧒🤠🤰") for _ in range(n_chars)
    ])
    print(f"  {label:{label_width}} {chars}   {value}")
