import sqlite3

conn = sqlite3.connect("database/consultbae.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    email TEXT UNIQUE,
    phone TEXT,
    city TEXT,
    skills TEXT,
    source TEXT
)
""")

conn.commit()
conn.close()

print("Database and people table created successfully.")