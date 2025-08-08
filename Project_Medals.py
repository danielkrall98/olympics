# How did the number of won medals differ before and after the fall of the Soviet Union?

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

# Filter the dataset to only include relevant events and countries
filtered_df = athletes_df[
    (athletes_df["Games"].isin(events_of_interest)) &
    (athletes_df["NOC"].isin(countries_of_interest)) &
    (athletes_df["Medal"].notna())  # Only include rows with medals
]

# Group by Games, NOC, and Medal type to count the number of medals
medal_counts = filtered_df.groupby(["Games", "NOC", "Medal"]).size().reset_index(name="Count")

# Prepare data for the bar chart
pre_fall_games = ["1988 Winter", "1988 Summer"]
post_fall_games = ["1994 Winter", "1996 Summer"]

# Pre-fall: Summing up only for "URS" (Soviet Union)
pre_fall_data = medal_counts[(medal_counts["Games"].isin(pre_fall_games)) & (medal_counts["NOC"] == "URS")]
pre_fall_summary = pre_fall_data.pivot_table(index="Games", columns="Medal", values="Count", aggfunc="sum", fill_value=0)

# Post-fall: Summing up medals for each country (successor states)
post_fall_data = medal_counts[medal_counts["Games"].isin(post_fall_games)]
post_fall_summary = post_fall_data.pivot_table(index="Games", columns="Medal", values="Count", aggfunc="sum", fill_value=0)

# Define fixed colors for medals
medal_colors = {
    "Gold": "gold", "Silver": "silver", "Bronze": "#cd7f32"
}

# Plotting
fig, ax = plt.subplots(figsize=(20, 12))

# Combine all data into a single plot
positions = []
labels = []
bar_width = 0.5  # Narrower bars to fit them side by side
gap = 1  # Add gaps between specific groups
current_position = 0
tick_positions = []

# Grid and other style elements are handled by the style applied earlier
ax.grid(axis='y', linestyle='-', linewidth=0.5, alpha=0.5, zorder=1)

# Process games in order
all_games = pre_fall_games + ["1992 Transition"] + post_fall_games

# Generate bar positions and labels
for idx, game in enumerate(all_games):
    if game == "1992 Transition":
        # Center the transition tick between 1988 Summer and 1994 Winter
        transition_position = current_position - (gap / 4)
        tick_positions.append(transition_position)
        labels.append(game)
        current_position += gap  # Add space after transition
        continue

    # Add bars for each medal type
    for i, medal in enumerate(["Gold", "Silver", "Bronze"]):
        if game in pre_fall_games:
            summary = pre_fall_summary
        elif game in post_fall_games:
            summary = post_fall_summary
        else:
            continue
        count = summary.loc[game, medal] if game in summary.index and medal in summary.columns else 0
        ax.bar(current_position + i * bar_width, count, width=bar_width, color=medal_colors[medal], label=medal if current_position == 0 else "", zorder=2)

    # Mark group center for ticks
    tick_positions.append(current_position + bar_width)
    labels.append(game)

    current_position += 3 * bar_width + gap  # Advance position for the next group

# Add vertical dotted line for 1992 Transition
ax.axvline(x=transition_position, color="gray", linestyle="--", label="1992 Transition")

# Final adjustments
ax.set_xticks(tick_positions)
ax.set_xticklabels(labels, rotation=45)
ax.set_ylabel("Number of Medals")
ax.set_title("Olympic Medal Counts: Pre- and Post-Fall of the Soviet Union")
ax.legend(title="Medal Types", bbox_to_anchor=(1, 1), loc="upper left")

plt.tight_layout()
plt.show()