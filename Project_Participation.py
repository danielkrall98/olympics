# How did the participations differ before and after the fall of the Soviet Union?

import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
athletes_file = "data/data_filtered.csv"
noc_file = "data/noc_regions.csv"

# Read data
athletes_df = pd.read_csv(athletes_file)
noc_df = pd.read_csv(noc_file)

# Define the years and events of interest
events_of_interest = [
    "1988 Winter", "1988 Summer", "1994 Winter", "1996 Summer"
]

# Define the countries of interest
countries_of_interest = [
    "URS", "RUS", "UKR", "LTU", "LAT", "EST", "GEO", "BLR", "MDA",
    "KGZ", "UZB", "TJK", "ARM", "AZE", "TKM", "KAZ"
]

# Filter the dataset
filtered_df = athletes_df[
    (athletes_df["Games"].isin(events_of_interest)) &
    (athletes_df["NOC"].isin(countries_of_interest))
]

# Group by Games and NOC for the count of athletes
athlete_counts = filtered_df.groupby(["Games", "NOC"]).size().reset_index(name="Count")

# Prepare data for the bar chart
pre_fall_games = ["1988 Winter", "1988 Summer"]
post_fall_games = ["1994 Winter", "1996 Summer"]

# Pre-fall: Summing up only for "URS"
pre_fall_data = athlete_counts[(athlete_counts["Games"].isin(pre_fall_games)) & (athlete_counts["NOC"] == "URS")]
pre_fall_summary = pre_fall_data.groupby("Games")["Count"].sum()

# Post-fall: Separate counts for each country
post_fall_data = athlete_counts[athlete_counts["Games"].isin(post_fall_games)]
post_fall_summary = post_fall_data.pivot(index="Games", columns="NOC", values="Count").fillna(0)

# Map NOC codes to country names
noc_mapping = noc_df.set_index("NOC")["region"].to_dict()
country_colors = {
    "RUS": "crimson", "UKR": "gold", "LTU": "lawngreen", "LAT": "maroon",
    "EST": "royalblue", "GEO": "silver", "BLR": "green", "MDA": "darkcyan",
    "KGZ": "pink", "UZB": "purple", "TJK": "orange", "ARM": "coral",
    "AZE": "navy", "TKM": "olivedrab", "KAZ": "aqua"
}
country_names = {noc: noc_mapping.get(noc, noc) for noc in country_colors.keys()}  # Map codes to names

# Plotting
fig, ax = plt.subplots(figsize=(20, 12))

# Combine all data into a single plot
positions = []
labels = []
bar_width = 0.6
current_position = 0

ax.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.7, zorder=1)

# Add pre-fall data
for game in pre_fall_games:
    positions.append(current_position)
    labels.append(game)
    height = pre_fall_summary.get(game, 0)
    bar = ax.bar(current_position, height, color="red", label="USSR" if current_position == 0 else "", zorder=2)
    
    # Add annotation for total count (no decimal places)
    ax.text(current_position, height + 3, str(int(height)), ha='center', va='bottom', fontsize=20)
    
    current_position += 1

# Add transition period
positions.append(current_position)
labels.append("1992 Transition")
current_position += 1

# Add post-fall data
already_plotted_countries = set()
for game in post_fall_games:
    positions.append(current_position)
    labels.append(game)
    bottom = 0
    total_height = 0
    for country in post_fall_summary.columns:
        count = post_fall_summary.loc[game, country] if game in post_fall_summary.index else 0
        label = country_names[country] if country not in already_plotted_countries else ""
        bar = ax.bar(current_position, count, color=country_colors[country], bottom=bottom, label=label, zorder=2)
        bottom += count
        total_height += count
        already_plotted_countries.add(country)
    
    # Add annotation for total count (no decimal places)
    ax.text(current_position, total_height + 3, str(int(total_height)), ha='center', va='bottom', fontsize=20)
    
    current_position += 1

# Add vertical dotted line for 1992 Transition
ax.axvline(x=len(pre_fall_games), color="gray", linestyle="--")

# Final adjustments
ax.set_xticks(positions)
ax.set_xticklabels(labels, rotation=45)
ax.set_ylabel("Number of Participations")
ax.set_title("Olympic Participation: Pre- and Post-Fall of the Soviet Union")
ax.legend(title="Countries", bbox_to_anchor=(1, 1), loc="upper left")

plt.tight_layout()
plt.show()