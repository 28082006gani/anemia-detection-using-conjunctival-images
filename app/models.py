import sqlite3
import os
import uuid
from flask import g, current_app

def get_db():
    if 'db' not in g:
        db_path = current_app.config['DATABASE_PATH']
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS scans (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        patient_name TEXT NOT NULL,
        patient_age INTEGER NOT NULL,
        patient_place TEXT NOT NULL,
        patient_city TEXT,
        patient_state TEXT,
        patient_country TEXT,
        image_filename TEXT NOT NULL,
        status TEXT NOT NULL,
        hemoglobin REAL NOT NULL,
        confidence REAL,
        is_placeholder INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_scans_user_id ON scans(user_id);
    CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
    """)

    # Safe migration for existing databases
    cursor = db.execute("PRAGMA table_info(scans)")
    columns = [row[1] for row in cursor.fetchall()]
    if 'patient_city' not in columns:
        db.execute("ALTER TABLE scans ADD COLUMN patient_city TEXT;")
    if 'patient_state' not in columns:
        db.execute("ALTER TABLE scans ADD COLUMN patient_state TEXT;")
    if 'patient_country' not in columns:
        db.execute("ALTER TABLE scans ADD COLUMN patient_country TEXT;")
    db.commit()

def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()

# User queries
def create_user(email: str, password_hash: str) -> dict:
    db = get_db()
    user_id = str(uuid.uuid4())
    db.execute(
        "INSERT INTO users (id, email, password_hash) VALUES (?, ?, ?)",
        (user_id, email.lower().strip(), password_hash)
    )
    db.commit()
    return {"id": user_id, "email": email.lower().strip()}

def get_user_by_email(email: str):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE email = ?",
        (email.lower().strip(),)
    ).fetchone()

def get_user_by_id(user_id: str):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

# Scan queries
def create_scan(user_id: str, patient_name: str, patient_age: int,
                patient_place: str, image_filename: str, status: str,
                hemoglobin: float, confidence: float = None, is_placeholder: bool = True,
                patient_city: str = None, patient_state: str = None, patient_country: str = None) -> str:
    db = get_db()
    scan_id = str(uuid.uuid4())

    # Fallback parse city/state/country from display place string if not provided
    if not patient_city and patient_place and ',' in patient_place:
        parts = [p.strip() for p in patient_place.split(',')]
        if len(parts) >= 2:
            patient_city = parts[0]
            patient_state = parts[1]
            if len(parts) >= 3:
                patient_country = parts[2]
            else:
                patient_country = 'India'

    db.execute(
        """
        INSERT INTO scans (
            id, user_id, patient_name, patient_age, patient_place,
            patient_city, patient_state, patient_country,
            image_filename, status, hemoglobin, confidence, is_placeholder
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            scan_id, user_id, patient_name.strip(), patient_age,
            patient_place.strip(), patient_city, patient_state, patient_country,
            image_filename, status,
            round(hemoglobin, 1), confidence, 1 if is_placeholder else 0
        )
    )
    db.commit()
    return scan_id

def get_scan_for_user(scan_id: str, user_id: str):
    """
    Core authorization rule: Query MUST filter by user_id.
    Returns scan row if owned by user, otherwise None.
    """
    db = get_db()
    return db.execute(
        "SELECT * FROM scans WHERE id = ? AND user_id = ?",
        (scan_id, user_id)
    ).fetchone()

def get_scans_for_user(user_id: str):
    db = get_db()
    return db.execute(
        "SELECT * FROM scans WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    ).fetchall()

def delete_scan_for_user(scan_id: str, user_id: str):
    db = get_db()
    scan = get_scan_for_user(scan_id, user_id)
    if not scan:
        return None
    db.execute(
        "DELETE FROM scans WHERE id = ? AND user_id = ?",
        (scan_id, user_id)
    )
    db.commit()
    return scan['image_filename']
