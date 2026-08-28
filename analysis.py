import sqlite3
import pandas as pd

conn = sqlite3.connect("cell_counts.db")

query = """
SELECT
    c.sample,
    totals.total_count,
    c.cell_type AS population,
    c.count,
    ROUND((c.count * 100.0) / totals.total_count, 2) AS percentage
FROM cell_counts c
JOIN (
    SELECT
        sample,
        SUM(count) AS total_count
    FROM cell_counts
    GROUP BY sample
) totals
ON c.sample = totals.sample
"""

summary = pd.read_sql_query(query, conn)

print(summary.head(10))

summary.to_csv("cell_frequencies.csv", index=False)

conn.close()

print("Part 2 analysis completed successfully.")