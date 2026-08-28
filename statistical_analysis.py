import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests


# Connect to the SQLite database
conn = sqlite3.connect("cell_counts.db")


# Get cell frequencies for melanoma patients
# receiving miraclib using PBMC samples
query = """
SELECT
    c.sample,
    c.cell_type AS population,
    c.count,
    s.condition,
    s.treatment,
    s.response,
    s.sample_type,
    (c.count * 100.0 / totals.total_count) AS percentage
FROM cell_counts c

JOIN samples s
    ON c.sample = s.sample

JOIN (
    SELECT
        sample,
        SUM(count) AS total_count
    FROM cell_counts
    GROUP BY sample
) totals
    ON c.sample = totals.sample

WHERE LOWER(s.condition) = 'melanoma'
  AND LOWER(s.treatment) = 'miraclib'
  AND UPPER(s.sample_type) = 'PBMC'
  AND LOWER(s.response) IN ('yes', 'no')
"""


# Read query result into pandas
df = pd.read_sql_query(query, conn)

conn.close()


# Save filtered Part 3 data
df.to_csv("part3_filtered_data.csv", index=False)


# Cell populations to analyze
cell_types = [
    "b_cell",
    "cd8_t_cell",
    "cd4_t_cell",
    "nk_cell",
    "monocyte"
]


# Store statistical results
results = []


# Analyze each cell population
for cell_type in cell_types:

    population_data = df[
        df["population"] == cell_type
    ]

    responders = population_data[
        population_data["response"].str.lower() == "yes"
    ]["percentage"]

    non_responders = population_data[
        population_data["response"].str.lower() == "no"
    ]["percentage"]


    # Welch's independent t-test
    t_stat, p_value = ttest_ind(
        responders,
        non_responders,
        equal_var=False
    )


    # Store results
    results.append({
        "population": cell_type,
        "responder_mean_percentage": responders.mean(),
        "non_responder_mean_percentage": non_responders.mean(),
        "t_statistic": t_stat,
        "p_value": p_value
    })


    # Create boxplot
    plt.figure(figsize=(6, 5))

    plt.boxplot(
        [responders, non_responders],
        tick_labels=[
            "Responders",
            "Non-responders"
        ]
    )

    plt.title(
        f"{cell_type}: Responders vs Non-responders"
    )

    plt.ylabel("Relative Frequency (%)")

    plt.tight_layout()

    plt.savefig(
        f"{cell_type}_boxplot.png"
    )

    plt.close()


# Convert results into a DataFrame
results_df = pd.DataFrame(results)


# Apply Benjamini-Hochberg FDR correction
results_df["adjusted_p_value"] = multipletests(
    results_df["p_value"],
    method="fdr_bh"
)[1]


# Determine significance after correction
results_df["significant_after_correction"] = (
    results_df["adjusted_p_value"] < 0.05
)


# Round values for readability
results_df["responder_mean_percentage"] = (
    results_df["responder_mean_percentage"].round(2)
)

results_df["non_responder_mean_percentage"] = (
    results_df["non_responder_mean_percentage"].round(2)
)

results_df["t_statistic"] = (
    results_df["t_statistic"].round(4)
)

results_df["p_value"] = (
    results_df["p_value"].round(6)
)

results_df["adjusted_p_value"] = (
    results_df["adjusted_p_value"].round(6)
)


# Save statistical results
results_df.to_csv(
    "statistical_results.csv",
    index=False
)


# Display all statistical results
print("\nStatistical Analysis Results:\n")

print(
    results_df.to_string(index=False)
)


# Display significant populations
print(
    "\nSignificant cell populations "
    "after FDR correction "
    "(adjusted p < 0.05):"
)

significant = results_df[
    results_df["significant_after_correction"] == True
]


if significant.empty:

    print(
        "No cell populations showed "
        "a significant difference."
    )

else:

    for population in significant["population"]:

        print(f"- {population}")


print(
    "\nPart 3 analysis completed successfully."
)