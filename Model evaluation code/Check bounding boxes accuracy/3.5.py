import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('output_data.csv')

# Group the data by the "label" column
grouped = df.groupby("label")

# Plot a line graph for each group
for name, group in grouped:
    plt.plot(group["image_id"], group["avg_distance"], label=name)

# Set the x- and y-axis labels and title
plt.xlabel("Image frame number")
plt.ylabel("Average distance")
plt.title("Average distance by label")

# Show the legend
plt.legend()

# Show the plot
plt.show()
