import sqlite3
import pandas as pd
import os
import sys

# Connect to database
conn = sqlite3.connect("database/consultbae.db")

# Read new CSV (supports optional CLI argument or defaults to source2_gig_workers.csv)
csv_path = sys.argv[1] if len(sys.argv) > 1 and os.path.exists(sys.argv[1]) else "data/source2_gig_workers.csv"
df = pd.read_csv(csv_path)

# Dynamic column mapping candidates
name_candidates = [
    "name", "full_name", "fullname", "candidate_name", "worker_name",
    "applicant_name", "person_name", "contact_name", "first_name"
]
phone_candidates = [
    "phone", "phone_number", "phonenumber", "mobile", "mobile_number",
    "mobilenumber", "contact", "contact_number", "contactnumber", "cell",
    "phone_no", "mobile_no"
]
email_candidates = [
    "email", "email_id", "emailid", "email_address", "emailaddress",
    "mail", "mail_id"
]
city_candidates = [
    "city", "location", "current_location", "currentlocation", "address", "town"
]
skills_candidates = [
    "skills", "skill_tags", "skilltags", "primary_skills", "primaryskills", "skill"
]

def find_column(df_columns, candidates):
    norm_map = {col.strip().lower().replace(" ", "_").replace("-", "_"): col for col in df_columns}
    for cand in candidates:
        norm_cand = cand.lower().replace(" ", "_").replace("-", "_")
        if norm_cand in norm_map:
            return norm_map[norm_cand]
    return None

name_col = find_column(df.columns, name_candidates)
phone_col = find_column(df.columns, phone_candidates)
email_col = find_column(df.columns, email_candidates)
city_col = find_column(df.columns, city_candidates)
skills_col = find_column(df.columns, skills_candidates)

# Check if required field (name) is missing
if not name_col:
    print(f"Error: Missing required column for name (e.g., 'name', 'full_name', 'worker_name') in CSV file '{csv_path}'.")
    sys.exit(1)

# Inspect DB schema dynamically
cursor = conn.execute("PRAGMA table_info(people)")
db_cols = [row[1] for row in cursor.fetchall()]
db_name_col = "full_name" if "full_name" in db_cols else "name"

duplicates = []
new_people = []

def get_clean_val(row, col_name):
    if col_name and col_name in row and pd.notna(row[col_name]):
        val = str(row[col_name]).strip()
        if val.lower() not in ("nan", "none", "null"):
            return val
    return ""

for _, row in df.iterrows():
    name_val = get_clean_val(row, name_col)
    phone_val = get_clean_val(row, phone_col)
    email_val = get_clean_val(row, email_col)
    city_val = get_clean_val(row, city_col)
    skills_val = get_clean_val(row, skills_col)

    # Build SQL query dynamically based on available fields
    conditions = []
    params = []

    if name_val:
        conditions.append(f"{db_name_col} = ?")
        params.append(name_val)
    if phone_val:
        conditions.append("phone = ?")
        params.append(phone_val)
    if email_val:
        conditions.append("email = ?")
        params.append(email_val)

    match = None
    if conditions:
        sql = f"SELECT * FROM people WHERE {' OR '.join(conditions)}"
        cursor = conn.execute(sql, tuple(params))
        match = cursor.fetchone()

    if match:
        row["is_duplicate"] = True
        duplicates.append(row)
    else:
        row["is_duplicate"] = False
        new_people.append(row)

        if "skills" in db_cols and "source" in db_cols:
            conn.execute(
                f"""
                INSERT INTO people({db_name_col}, email, phone, city, skills, source)
                VALUES(?, ?, ?, ?, ?, ?)
                """,
                (name_val, email_val, phone_val, city_val, skills_val, os.path.basename(csv_path))
            )
        else:
            conn.execute(
                f"""
                INSERT INTO people({db_name_col}, email, phone, city)
                VALUES(?, ?, ?, ?)
                """,
                (name_val, email_val, phone_val, city_val)
            )

conn.commit()

pd.DataFrame(duplicates).to_csv(
    "database/duplicates.csv",
    index=False
)

print("Duplicate check completed.")