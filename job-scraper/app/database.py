import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DATABASE_URL", "jobs.db")

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            location TEXT,
            keyword TEXT
        )
    """)

    conn.commit()
    conn.close()