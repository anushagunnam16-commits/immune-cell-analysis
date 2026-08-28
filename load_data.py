import sqlite3
import csv

DB_FILE = "cell_counts.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS samples (
    sample TEXT PRIMARY KEY,
    project TEXT,
    subject TEXT,
    condition TEXT,
    age INTEGER,
    sex TEXT,
    treatment TEXT,
    response TEXT,
    sample_type TEXT,
    time_from_treatment_start INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cell_counts (
    sample TEXT,
    cell_type TEXT,
    count INTEGER,
    FOREIGN KEY (sample) REFERENCES samples(sample)
)
""")
cursor.execute("DELETE FROM cell_counts")
cursor.execute("DELETE FROM samples")

with open("cell-count.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        cursor.execute("""
        INSERT OR REPLACE INTO samples (
            sample,
            project,
            subject,
            condition,
            age,
            sex,
            treatment,
            response,
            sample_type,
            time_from_treatment_start
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["sample"],
            row["project"],
            row["subject"],
            row["condition"],
            int(row["age"]),
            row["sex"],
            row["treatment"],
            row["response"],
            row["sample_type"],
            int(row["time_from_treatment_start"])
        ))

        cell_types = [
            "b_cell",
            "cd8_t_cell",
            "cd4_t_cell",
            "nk_cell",
            "monocyte"
        ]

        for cell_type in cell_types:
            cursor.execute("""
            INSERT INTO cell_counts (
                sample,
                cell_type,
                count
            )
            VALUES (?, ?, ?)
            """, (
                row["sample"],
                cell_type,
                int(row[cell_type])
            ))

conn.commit()
conn.close()

print("Database created and data loaded successfully.")