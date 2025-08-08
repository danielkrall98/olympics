# Participations per Medal
# How many participations were required on average to win a medal?

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
    "1988 Winter", "1988 Summer", "1992 Transition", "1994 Winter", "1996 Summer"
]

# Define the countries of interest
countries_of_interest = [
    "URS", "RUS", "UKR", "LTU", "LAT", "EST", "GEO", "BLR", "MDA",
    "KGZ", "UZB", "TJK", "ARM", "AZE", "TKM", "KAZ"
]

# Filter the dataset for participation
participation_df = athletes_df[
    (athletes_df["Games"].isin(events_of_interest)) &
    (athletes_df["NOC"].isin(countries_of_interest))
]

# Count participations
participation_counts = participation_df.groupby(["Games", "NOC"]).size().reset_index(name="Participation_Count")

# Filter the dataset for medals
medal_df = athletes_df[
    (athletes_df["Games"].isin(events_of_interest)) &
    (athletes_df["NOC"].isin(countries_of_interest)) &
    (athletes_df["Medal"].notna())
]

# Count medals
medal_counts = medal_df.groupby(["Games", "NOC"]).size().reset_index(name="Medal_Count")

# Merge participation and medal data
combined_data = pd.merge(
    participation_counts, medal_counts, on=["Games", "NOC"], how="outer"
).fillna(0)

# Calculate total participations and medals for pre- and post-fall
pre_fall_games = ["1988 Winter", "1988 Summer"]
post_fall_games = ["1994 Winter", "1996 Summer"]

pre_fall_data = combined_data[combined_data["Games"].isin(pre_fall_games) & (combined_data["NOC"] == "URS")]
post_fall_data = combined_data[combined_data["Games"].isin(post_fall_games)]

# Summing up pre-fall data
pre_fall_summary = pre_fall_data.groupby("Games").sum()[["Participation_Count", "Medal_Count"]]
pre_fall_summary["Avg_Participation_Per_Medal"] = (
    pre_fall_summary["Participation_Count"] / pre_fall_summary["Medal_Count"]
)

# Summing up post-fall data (combining all successor states)
post_fall_summary = post_fall_data.groupby("Games").sum()[["Participation_Count", "Medal_Count"]]
post_fall_summary["Avg_Participation_Per_Medal"] = (
    post_fall_summary["Participation_Count"] / post_fall_summary["Medal_Count"]
)

# Combine pre-fall and post-fall summaries
summary = pd.concat([pre_fall_summary, post_fall_summary])

# Add 1992 Transition manually (without data point)
summary.loc["1992 Transition"] = [None, None, None]

fig, ax = plt.subplots(figsize=(20, 12))

ax.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.7, zorder=1)

# Properly map X-axis
x_positions = [0, 1, 3, 4]
events_order = ["1988 Winter", "1988 Summer", "1994 Winter", "1996 Summer"]

# Reorder summary_excluding_transition to match events_order
summary_excluding_transition = summary.dropna(subset=["Avg_Participation_Per_Medal"]).reindex(events_order)

# Plot the data points
ax.plot(
    x_positions,
    summary_excluding_transition["Avg_Participation_Per_Medal"].values,
    marker="o",
    linestyle="-",
    color="crimson",
    label="Average Participations per Medal",
    linewidth=5,  # Makes the line wider
    markersize=15  # Makes the points bigger
)

# Add annotations
for idx, row in summary_excluding_transition.iterrows():
    value = row["Avg_Participation_Per_Medal"]
    x_pos = x_positions[events_order.index(idx)]
    ax.annotate(
        f"{value:.2f}",
        (x_pos, value),
        textcoords="offset points",
        xytext=(0, 30),
        ha="center",
        fontsize=20,
        color="black"
    )

# Mark 1992 Transition
ax.axvline(x=2, color="gray", linestyle="--", label="1992 Transition")

# Final adjustments
ax.set_ylim(0, max(summary_excluding_transition["Avg_Participation_Per_Medal"]) * 1.2)
ax.set_xticks(x_positions)
ax.set_xticklabels(events_order, rotation=45)
ax.set_ylabel("Average Participations per Medal")
ax.set_title("Average Number of Participations Required to Win a Medal")
ax.legend()

plt.tight_layout()
plt.show()