ConsultBae AI Automation Assignment
Overview

This project contains solutions for the ConsultBae AI Automation Take-Home Assignment.

Completed Tasks:

Task 1 - CSV Merge
Task 2 - n8n Automation
Task 3 - Audio Collection Web App
Task 4 - Data Issues Report
Tech Stack
Python
Flask
SQLite
SQLAlchemy
HTML
n8n
Mutagen
SoundFile
Librosa
Features
CSV Merge
Imported three CSV files
Cleaned duplicate records
Stored merged data into SQLite
Automation

Built an n8n workflow that

accepts new CSV
checks duplicates
stores data

Workflow JSON included.

Audio App

Users can

Enter Name
Enter Phone
Upload audio

Automatically extracts

Duration
Sample Rate
Bitrate
Loudness

Displays

Audio player
Metadata
Submission history
Installation
git clone <repo-url>


cd consultbae-assignment


pip install -r requirements.txt


python app.py

Visit

http://127.0.0.1:5000
Project Structure
app.py


models.py


templates/


uploads/


database/


scripts/


requirements.txt
Data Issues Report

See

DATA_ISSUES_REPORT.md
Stuck Log

See

STUCK_LOG.md
Video

Demo video included with submission.