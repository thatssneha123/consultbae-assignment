# STUCK_LOG.md

# ConsultBae AI Automation Assignment

## Challenges Encountered

### Task 1 – CSV Merge

**Challenge**
The three CSV files contained different column names, duplicate records, missing values, and inconsistent phone number formats.

**Resolution**
- Standardized column names.
- Removed duplicate entries.
- Filled or handled missing values.
- Normalized phone number formatting before merging.

---

### Task 2 – n8n Workflow

**Challenge**
Configuring the workflow to automatically process uploaded CSV files and avoid importing duplicates.

**Resolution**
- Created an n8n workflow that imports CSV files.
- Added duplicate checking logic.
- Stored cleaned records into the SQLite database.

---

### Task 3 – Audio Metadata Web App

**Challenge**
Extracting metadata from uploaded audio files with different formats.

**Resolution**
- Used Mutagen and Librosa libraries.
- Supported multiple audio formats.
- Displayed extracted metadata in the Flask application.

---

### Task 4 – Data Quality Report

**Challenge**
Generating a report that summarizes data quality issues after merging datasets.

**Resolution**
- Identified duplicate records.
- Reported missing values.
- Detected inconsistent phone numbers.
- Highlighted formatting inconsistencies.
- Exported the report as CSV.

---

## Git & Repository

### Challenge

Learning Git commands, creating a GitHub repository, and organizing the repository correctly.

### Resolution

- Created a public GitHub repository.
- Added a detailed README.
- Added a .gitignore file.
- Committed changes using meaningful commit messages.
- Uploaded the complete project to GitHub.

---

## Overall Learning

This assignment improved my understanding of:

- Data cleaning with Python and Pandas
- SQLite database integration
- Flask web development
- Audio metadata extraction
- n8n workflow automation
- Git and GitHub version control
- Project documentation