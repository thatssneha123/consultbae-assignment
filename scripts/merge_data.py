import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
from sqlalchemy.orm import sessionmaker

from models import engine, Person

from scripts.clean_data import (
    clean_name,
    clean_email,
    clean_phone,
    clean_city,
    clean_status,
    clean_verified,
    clean_skills,
)

# ---------------------------------------------------
# Read Data
# ---------------------------------------------------

naukri = pd.read_csv("data/source1_naukri_applicants copy.csv")
gig = pd.read_csv("data/source2_gig_workers.csv")
cb = pd.read_csv("data/source3_cbnexus_contacts.csv")

# ---------------------------------------------------
# Standardize Dataset 1
# ---------------------------------------------------

naukri = pd.DataFrame({
    "name": naukri["Full Name"].apply(clean_name),
    "email": naukri["Email"].apply(clean_email),
    "phone": naukri["Phone"].apply(clean_phone),
    "city": naukri["City"].apply(clean_city),

    "experience": naukri["Experience (Years)"],
    "current_ctc": naukri["Current CTC"],
    "applied_date": naukri["Applied Date"],

    "skills": naukri["Skills"].apply(clean_skills),

    "hourly_rate": None,
    "worker_status": None,

    "verified": None,
    "projects_completed": None,

    "source": "Naukri"
})

# ---------------------------------------------------
# Standardize Dataset 2
# ---------------------------------------------------

gig = pd.DataFrame({

    "name": gig["worker_name"].apply(clean_name),

    "email": gig["email_id"].apply(clean_email),

    "phone": None,

    "city": gig["location"].apply(clean_city),

    "experience": None,

    "current_ctc": None,

    "applied_date": None,

    "skills": gig["skill_tags"].apply(clean_skills),

    "hourly_rate": gig["rate"],

    "worker_status": gig["status"].apply(clean_status),

    "verified": None,

    "projects_completed": None,

    "source": "Gig Workers"

})

# ---------------------------------------------------
# Standardize Dataset 3
# ---------------------------------------------------

cb = pd.DataFrame({

    "name": cb["Name"].apply(clean_name),

    "email": None,

    "phone": cb["Phone Number"].apply(clean_phone),

    "city": cb["City"].apply(clean_city),

    "experience": None,

    "current_ctc": None,

    "applied_date": None,

    "skills": None,

    "hourly_rate": None,

    "worker_status": None,

    "verified": cb["Verified"].apply(clean_verified),

    "projects_completed": pd.to_numeric(
        cb["Projects Completed"],
        errors="coerce"
    ),

    "source": "CB Nexus"

})

# ---------------------------------------------------
# Merge
# ---------------------------------------------------

merged = pd.concat(
    [naukri, gig, cb],
    ignore_index=True
)

# ---------------------------------------------------
# Match Key
# ---------------------------------------------------

def create_match_key(row):

    if pd.notna(row["email"]):
        return f"EMAIL_{row['email']}"

    if pd.notna(row["phone"]):
        return f"PHONE_{row['phone']}"

    return f"NAMECITY_{row['name']}_{row['city']}"

merged["match_key"] = merged.apply(create_match_key, axis=1)

# ---------------------------------------------------
# Data Quality Report
# ---------------------------------------------------

duplicate_rows = merged[
    merged.duplicated("match_key", keep=False)
]

duplicate_rows.to_csv(
    "database/data_quality_report.csv",
    index=False
)

# ---------------------------------------------------
# Remove Duplicates
# ---------------------------------------------------

merged = merged.drop_duplicates(
    subset="match_key",
    keep="first"
)

merged = merged.drop(columns=["match_key"])

# ---------------------------------------------------
# Save CSV
# ---------------------------------------------------

merged.to_csv(
    "database/merged_people.csv",
    index=False
)

# ---------------------------------------------------
# Save SQLite
# ---------------------------------------------------

Session = sessionmaker(bind=engine)
session = Session()

session.query(Person).delete()
session.commit()

def clean_val(val):
    return None if pd.isna(val) else val

for _, row in merged.iterrows():

    session.add(

        Person(

            name=clean_val(row["name"]),
            email=clean_val(row["email"]),
            phone=clean_val(row["phone"]),
            city=clean_val(row["city"]),

            experience=clean_val(row["experience"]),
            current_ctc=clean_val(row["current_ctc"]),
            applied_date=clean_val(row["applied_date"]),

            skills=clean_val(row["skills"]),

            hourly_rate=clean_val(row["hourly_rate"]),
            worker_status=clean_val(row["worker_status"]),

            verified=clean_val(row["verified"]) if pd.isna(row["verified"]) else bool(row["verified"]),
            projects_completed=clean_val(row["projects_completed"]) if pd.isna(row["projects_completed"]) else int(row["projects_completed"]),

            source=clean_val(row["source"])

        )

    )

session.commit()

print("="*60)
print("CONSULTBAE DATA MERGE REPORT")
print("="*60)
print(f"Original Records : {105}")
print(f"Unique Records   : {len(merged)}")
print(f"Duplicates Found : {105-len(merged)}")
print("="*60)

print("\nGenerated Files")
print("-------------------------")
print("database/consultbae.db")
print("database/merged_people.csv")
print("database/data_quality_report.csv")