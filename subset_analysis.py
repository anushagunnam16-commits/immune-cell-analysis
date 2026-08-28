import sqlite3
import pandas as pd


# Connect to SQLite database
conn = sqlite3.connect("cell_counts.db")


# --------------------------------------------------
# PART 4.1
# Melanoma + PBMC + baseline + Miraclib samples
# --------------------------------------------------

query = """
SELECT *
FROM samples
WHERE LOWER(condition) = 'melanoma'
  AND UPPER(sample_type) = 'PBMC'
  AND time_from_treatment_start = 0
  AND LOWER(treatment) = 'miraclib'
"""

baseline_df = pd.read_sql_query(query, conn)


print("\n--- Baseline Melanoma PBMC Miraclib Samples ---")

print("Total baseline samples:", len(baseline_df))


# Save the filtered samples
baseline_df.to_csv(
    "baseline_melanoma_pbmc_miraclib.csv",
    index=False
)


# --------------------------------------------------
# PART 4.2.1
# Number of samples from each project
# --------------------------------------------------

project_counts = baseline_df["project"].value_counts()

print("\nSamples from each project:")
print(project_counts)


# --------------------------------------------------
# PART 4.2.2
# Number of subjects who were responders
# and non-responders
# --------------------------------------------------

response_counts = (
    baseline_df
    .groupby("response")["subject"]
    .nunique()
)

print("\nSubjects by response:")
print(response_counts)


# --------------------------------------------------
# PART 4.2.3
# Number of male and female subjects
# --------------------------------------------------

sex_counts = (
    baseline_df
    .groupby("sex")["subject"]
    .nunique()
)

print("\nSubjects by sex:")
print(sex_counts)


# --------------------------------------------------
# FINAL QUESTION
# Average B-cell count for:
# melanoma
# male
# responder
# time = 0
#
# All sample types and treatments are included.
# --------------------------------------------------

b_cell_query = """
SELECT AVG(c.count) AS average_b_cell_count
FROM cell_counts c
JOIN samples s
    ON c.sample = s.sample
WHERE LOWER(s.condition) = 'melanoma'
  AND UPPER(s.sex) = 'M'
  AND LOWER(s.response) = 'yes'
  AND s.time_from_treatment_start = 0
  AND c.cell_type = 'b_cell'
"""

b_cell_result = pd.read_sql_query(
    b_cell_query,
    conn
)

average_b_cells = b_cell_result[
    "average_b_cell_count"
].iloc[0]


print(
    "\nAverage B-cell count for male melanoma "
    "responders at time 0:"
)

print(f"{average_b_cells:.2f}")


# Close database connection
conn.close()


print("\nPart 4 analysis completed successfully.")