import matplotlib

# Use the 'kitty' backend
matplotlib.use("module://matplotlib-backend-kitty")

# A matplotlib example downloaded from the gallery
import matplotlib.pyplot as plt
import polars as pl

cities = pl.read_parquet("data/cities.parquet")

fig, ax = plt.subplots()

ax.scatter(cities["lng"], cities["lat"])
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Map of the World")
# fig.patch.set_facecolor('white')
plt.show()
