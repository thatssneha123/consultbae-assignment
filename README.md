# ConsultBae AI Automation Assignment

## Overview

This repository contains my solution for the **ConsultBae AI Automation Take-Home Assignment**.

The project includes:

- CSV data merging and cleaning
- Duplicate detection
- SQLite database creation
- n8n automation workflow
- Flask audio submission web application
- Automatic audio metadata extraction
- Data quality report

---

# Tech Stack

- Python
- Flask
- SQLite
- SQLAlchemy
- HTML/CSS
- n8n
- Librosa
- SoundFile
- Pandas

---

# Project Structure

```
consultbae-assignment/
│
├── app.py
├── models.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── source1_naukri_applicants.csv
│   ├── source2_gig_workers.csv
│   └── source3_cbnexus_contacts.csv
│
├── database/
│   ├── people.db
│   ├── consultbae.db
│   ├── import_data.py
│   ├── database.py
│   ├── check_duplicates.py
│   ├── merged_people.csv
│   ├── duplicates.csv
│   └── data_quality_report.csv
│
├── scripts/
│   ├── clean_data.py
│   ├── merge_data.py
│   ├── inspect_data.py
│   └── test_cleaning.py
│
├── templates/
│
└── uploads/
```

---

# Task 1 – CSV Merge

Implemented a data pipeline that:

- Imports all three CSV files
- Cleans inconsistent records
- Removes duplicate people
- Merges data into a single dataset
- Stores final records inside SQLite

---

# Task 2 – n8n Automation

Created an n8n workflow that:

- Accepts a new CSV
- Checks duplicate entries
- Imports cleaned records
- Saves data into the database

The workflow JSON file is included in the repository.

---

# Task 3 – Audio Collection Web App

The Flask application allows users to:

- Enter name
- Enter phone number
- Upload audio
- Store submissions in the database

For every upload the application automatically extracts:

- Duration
- Sample Rate
- Bitrate
- Loudness

The application also provides a submissions page with:

- Audio player
- Duration
- Sample rate
- Bitrate
- Loudness

---

# Task 4 – Data Issues Report

The following data issues were identified:

- Duplicate records
- Missing values
- Inconsistent phone numbers
- Different name formats
- Empty fields

These were cleaned during preprocessing and documented in the project.

---

# Installation

Clone the repository

```bash
git clone https://github.com/thatssneha123/consultbae-assignment.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

## Stuck Log

A detailed development log is available in STUCK_LOG.md.

Summary:
- CSV merge: standardized column names and handled duplicates.
- n8n workflow: resolved CSV parsing and database import issues.
- Audio upload: fixed Flask file handling and metadata extraction.

# Author

Sneha Shivangi`