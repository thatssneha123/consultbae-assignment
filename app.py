from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
import sqlite3
import pandas as pd
import os
import math
import numpy as np
import soundfile as sf
import librosa
import mutagen
from werkzeug.utils import secure_filename

app = Flask(__name__)

DATABASE = "database/consultbae.db"
UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_connection():
    return sqlite3.connect(DATABASE)


def init_audio_db():
    conn = get_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS audio_submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        audio_path TEXT,
        duration REAL,
        sample_rate INTEGER,
        bitrate INTEGER,
        loudness REAL
    )
    """)
    conn.commit()
    conn.close()


init_audio_db()


def extract_audio_metadata(filepath):
    duration = 0.0
    sample_rate = 0
    bitrate = 0
    loudness = -100.0

    # 1. Extract metadata via Mutagen
    try:
        mut_file = mutagen.File(filepath)
        if mut_file and mut_file.info:
            info = mut_file.info
            if hasattr(info, 'length') and info.length:
                duration = float(info.length)
            if hasattr(info, 'sample_rate') and info.sample_rate:
                sample_rate = int(info.sample_rate)
            if hasattr(info, 'bitrate') and info.bitrate:
                raw_bitrate = int(info.bitrate)
                bitrate = raw_bitrate // 1000 if raw_bitrate > 1000 else raw_bitrate
    except Exception as e:
        print("Mutagen extraction note:", e)

    # 2. Extract metadata via Soundfile
    try:
        sf_info = sf.info(filepath)
        if not duration:
            duration = float(sf_info.duration)
        if not sample_rate:
            sample_rate = int(sf_info.samplerate)
        if not bitrate and sample_rate:
            channels = getattr(sf_info, 'channels', 1)
            bitrate = (sample_rate * channels * 16) // 1000
    except Exception as e:
        print("Soundfile extraction note:", e)

    # 3. Extract metadata via Librosa (and calculate RMS Loudness in dB)
    try:
        y, sr = librosa.load(filepath, sr=None)
        if not duration and len(y) > 0 and sr > 0:
            duration = float(len(y) / sr)
        if not sample_rate and sr > 0:
            sample_rate = int(sr)

        if len(y) > 0:
            rms = float(np.mean(librosa.feature.rms(y=y)))
            if rms > 1e-9:
                loudness = float(20 * math.log10(rms))
            else:
                loudness = -100.0
    except Exception as e:
        print("Librosa extraction note:", e)

    return {
        "duration": round(duration, 2),
        "sample_rate": int(sample_rate),
        "bitrate": int(bitrate),
        "loudness": round(loudness, 2)
    }


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        audio_file = request.files.get("audio") or request.files.get("audio_file")

        if audio_file and audio_file.filename:
            filename = secure_filename(audio_file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            audio_file.save(filepath)

            metadata = extract_audio_metadata(filepath)
            saved_rel_path = f"uploads/{filename}"

            conn = get_connection()
            conn.execute("""
            INSERT INTO audio_submissions
            (name, phone, audio_path, duration, sample_rate, bitrate, loudness)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                name,
                phone,
                saved_rel_path,
                metadata["duration"],
                metadata["sample_rate"],
                metadata["bitrate"],
                metadata["loudness"]
            ))
            conn.commit()
            conn.close()

            return redirect(url_for("submissions"))

    return render_template("index.html")


@app.route("/submissions")
def submissions():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audio_submissions ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return render_template("submissions.html", submissions=rows)


@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/check-duplicates", methods=["POST"])
def check_duplicates():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    is_single = False
    if isinstance(data, dict):
        is_single = True
        items = [data]
    elif isinstance(data, list):
        items = data
    else:
        return jsonify({"error": "Invalid JSON payload"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    duplicates = []
    new_records = []

    for person in items:
        if not isinstance(person, dict):
            continue

        email = str(person.get("email") or person.get("email_id") or "").strip().lower()
        phone = str(person.get("phone") or person.get("phone_number") or person.get("mobile") or "").strip()
        name = str(person.get("full_name") or person.get("name") or person.get("worker_name") or "").strip()

        conditions = []
        params = []
        if email:
            conditions.append("lower(email)=?")
            params.append(email)
        if phone:
            conditions.append("phone=?")
            params.append(phone)
        if name:
            conditions.append("lower(full_name)=?")
            params.append(name.lower())

        if conditions:
            query = "SELECT 1 FROM people WHERE " + " OR ".join(conditions)
            cursor.execute(query, tuple(params))
            existing = cursor.fetchone()
        else:
            existing = None

        if existing:
            person["is_duplicate"] = True
            duplicates.append(person)
        else:
            person["is_duplicate"] = False
            full_name = person.get("full_name") or person.get("name") or person.get("worker_name") or ""

            cursor.execute("""
            INSERT INTO people
            (full_name,email,phone,city,skills,source)
            VALUES(?,?,?,?,?,?)
            """, (
                full_name,
                email,
                phone,
                person.get("city", ""),
                person.get("skills", ""),
                person.get("source", "n8n")
            ))

            new_records.append(person)

    conn.commit()
    conn.close()

    res = {
        "duplicates": duplicates,
        "new_records": new_records,
        "duplicates_found": len(duplicates),
        "inserted": len(new_records)
    }

    if is_single:
        res["duplicate"] = (len(duplicates) > 0)

    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True)