import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

files = {
    "Naukri Applicants": BASE_DIR / "data" / "source1_naukri_applicants copy.csv",
    "Gig Workers": BASE_DIR / "data" / "source2_gig_workers.csv",
    "CB Nexus Contacts": BASE_DIR / "data" / "source3_cbnexus_contacts.csv",
}

for dataset_name, file_path in files.items():

    print("=" * 80)
    print(f"{dataset_name}")
    print("=" * 80)

    df = pd.read_csv(file_path)

    print(f"\nRows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumn Names")
    print("-" * 40)
    print(df.columns.tolist())

    print("\nData Types")
    print("-" * 40)
    print(df.dtypes)

    print("\nMissing Values")
    print("-" * 40)
    print(df.isnull().sum())

    print("\nDuplicate Rows")
    print("-" * 40)
    print(df.duplicated().sum())

    print("\nFirst Five Records")
    print("-" * 40)
    print(df.head())

    print("\n")