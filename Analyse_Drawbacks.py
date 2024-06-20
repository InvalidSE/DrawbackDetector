import pandas
import numpy as np

# Load the data
data = pandas.read_json("./drawbacks.json")
data = data["drawbacks"].apply(pandas.Series)

# print(data.head())
print(data)

# Analyse frequency of drawbacks
drawback_freq = data.groupby("title").size().sort_values(ascending=False)
print(drawback_freq)

# Output to CSV
drawback_freq.to_csv("./drawback_freq.csv")
drawback_freq.name = 'drawback_frequency'

# Sort data by frequency
data = data.merge(drawback_freq, left_on="title", right_index=True)
data = data.sort_values(by="drawback_frequency", ascending=False)

# Remove if description is also a duplicate
data = data.drop_duplicates(subset=["title", "description"])

# Output to CSV
data.to_csv("./drawbacks.csv")
