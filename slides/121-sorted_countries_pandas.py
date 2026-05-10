import pandas as pd

df = pd.read_csv("data/countries.csv")
df = df[df["region"] == "Asia"].sort_values("population", ascending=False)
print(df)
