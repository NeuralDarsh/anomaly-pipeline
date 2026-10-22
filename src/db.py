import sqlite3
from pathlib import Path

DB_PATH = Path("data/pipeline.db")


def get_conn():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric TEXT,
            ts TEXT,
            value REAL,
            zscore REAL,
            is_anomaly INTEGER,
            severity TEXT
        )
    """)
    return conn


def save(conn, metric, ts, value, z, is_anomaly, severity):
    conn.execute(
        "INSERT INTO results (metric, ts, value, zscore, is_anomaly, severity) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (metric, ts, value, z, int(is_anomaly), severity),
    )