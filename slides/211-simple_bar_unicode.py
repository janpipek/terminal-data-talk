import polars as pl

print()

# HIDE_ABOVE
countries = (
    pl.read_csv("data/countries.csv")
    .filter(region="Asia")
    .sort("population", descending=True)
    .select("country", "population")
)
countries = countries.head(15)
data = {country: population for country, population in countries.iter_rows()}

# Some measurements
MAX_BAR_WIDTH = 40  # HIDE
label_width = max(len(label) for label in data)
max_value = max(data.values())

# Draw line of various widths
for label, value in data.items():
    n_chars = max(int(value / max_value * WIDTH / 2), 1)
    print(f"  {label:{label_width}} {'█' * n_chars}   {value}")
