# models/data_storage.py
import sqlite3
import json
import pandas as pd

def init_db(db_path="ai_brain_data.db"):
    """
    Initialize or connect to SQLite database for AI brain data storage.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS ai_brain_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT,
            prediction TEXT,
            actual TEXT,
            features TEXT,
            confidence REAL,
            meta TEXT,
            processed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
    print(f"[M4] Database initialized at {db_path}")

def insert_record(input_text, prediction, features=None, confidence=None, meta=None, db_path="ai_brain_data.db"):
    """
    Insert a record into AI brain database.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        INSERT INTO ai_brain_data (input_text, prediction, features, confidence, meta)
        VALUES (?, ?, ?, ?, ?)
    """, (
        input_text,
        prediction,
        json.dumps(features or {}),
        confidence,
        json.dumps(meta or {})
    ))
    conn.commit()
    record_id = c.lastrowid
    conn.close()
    print(f"[M4] Record saved with ID {record_id}")
    return record_id

def update_record_actual(record_id, actual, mark_processed=True, db_path="ai_brain_data.db"):
    """
    Update actual (true) value for a prediction, mark as processed if needed.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        UPDATE ai_brain_data
        SET actual=?, processed=?
        WHERE id=?
    """, (actual, 1 if mark_processed else 0, record_id))
    conn.commit()
    conn.close()
    print(f"[M4] Record {record_id} updated with actual result.")

def fetch_unprocessed(limit=10, db_path="ai_brain_data.db"):
    """
    Fetch unprocessed records for review or retraining.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        SELECT id, input_text, prediction, actual, features, confidence, meta
        FROM ai_brain_data
        WHERE processed=0
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = c.fetchall()
    conn.close()
    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "input_text": r[1],
            "prediction": r[2],
            "actual": r[3],
            "features": json.loads(r[4] or "{}"),
            "confidence": r[5],
            "meta": json.loads(r[6] or "{}")
        })
    return result

def export_to_csv(file_path="training_data.csv", include_unprocessed_only=False, db_path="ai_brain_data.db"):
    """
    Export database records to a CSV file for AI retraining.
    """
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM ai_brain_data"
    if include_unprocessed_only:
        query += " WHERE processed=0"
    df = pd.read_sql_query(query, conn)
    df.to_csv(file_path, index=False)
    conn.close()
    print(f"[M4] Data exported to {file_path}")
