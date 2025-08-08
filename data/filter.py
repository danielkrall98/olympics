import pandas as pd

# Load the dataset
input_file = "athlete_events.csv"  # Path to your input CSV file
output_file = "filtered_athletes.csv"  # Path to the output CSV file

# Define the NOCs and Games of interest
countries_of_interest = [
    "URS", "RUS", "UKR", "LTU", "LAT", "EST", "GEO", "BLR", "MDA",
    "KGZ", "UZB", "TJK", "ARM", "AZE", "TKM", "KAZ"
]
games_of_interest = ["1988 Winter", "1988 Summer", "1994 Winter", "1996 Summer"]

# Read the CSV file
df = pd.read_csv(input_file)

# Filter based on NOCs and Games
filtered_df = df[
    (df["NOC"].isin(countries_of_interest)) &
    (df["Games"].isin(games_of_interest))
]

# Sort the data by NOC and Games
sorted_df = filtered_df.sort_values(by=["NOC", "Games"])

# Save the filtered and sorted data to a new CSV file
sorted_df.to_csv(output_file, index=False)

print(f"Filtered and sorted data has been saved to '{output_file}'.")