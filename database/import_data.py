import pandas as pd
import sqlite3
import os

# CSV files
files = [
    "data/source1_naukri_applicants copy.csv",
    "data/source2_gig_workers.csv",
    "data/source3_cbnexus_contacts.csv"
]

all_data = []

for file in files:
    df = pd.read_csv(file)

    # Normalize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Create standard columns if missing
    for col in ["full_name", "email", "phone", "city", "skills"]:
        if col not in df.columns:
            df[col] = ""

    df["source"] = os.path.basename(file)

    all_data.append(df[["full_name", "email", "phone", "city", "skills", "source"]])

# Merge all records
people = pd.concat(all_data, ignore_index=True)

# Clean text
people = people.fillna("")
people["email"] = people["email"].str.lower().str.strip()
people["phone"] = people["phone"].astype(str).str.strip()

# Remove duplicates
people = people.drop_duplicates(subset=["email"], keep="first")

# Save merged CSV
people.to_csv("database/merged_people.csv", index=False)

# Insert into SQLite
conn = sqlite3.connect("database/consultbae.db")

people.to_sql(
    "people",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Imported", len(people), "people successfully.")