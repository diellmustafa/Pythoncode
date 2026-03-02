from uuid import uuid4
from passlib.context import CryptContext
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import sqlite3
from .models import UserCreate, UserLogin, Job
from .database import create_table, get_connection
from .scraper import scrape_jobs

app = FastAPI(title="Job Scraper API")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create base tables
create_table()

# =========================
# INIT SAVED JOBS TABLE
# =========================
def init_saved_jobs():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            job_id INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_saved_jobs()

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {"message": "Job Scraper API is running"}

# =========================
# SCRAPER (FIXED)
# =========================
@app.post("/scrape/{keyword}")
def scrape(keyword: str, username: str = Query(...)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    db_user = cursor.fetchone()

    if not db_user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    user_id = db_user["id"]
    conn.close()

    jobs = scrape_jobs(keyword, user_id)
    return {"scraped_jobs": len(jobs)}

# =========================
# GET ALL JOBS
# =========================
@app.get("/jobs")
def get_jobs(username: str = Query(...)):
    conn = get_connection()
    cursor = conn.cursor()

    # Get user
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    db_user = cursor.fetchone()

    if not db_user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    user_id = db_user["id"]

    # Fetch ONLY that user's jobs
    cursor.execute(
        "SELECT * FROM jobs WHERE user_id = ?",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

# =========================
# REGISTER
# =========================
@app.post("/register")
def register(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return {"error": "Username already exists"}

    hashed_password = pwd_context.hash(user.password)
    user_id = str(uuid4())

    cursor.execute(
        "INSERT INTO users (id, username, password) VALUES (?, ?, ?)",
        (user_id, user.username, hashed_password)
    )

    conn.commit()
    conn.close()

    return {"message": "User registered successfully"}

# =========================
# LOGIN
# =========================
@app.post("/login")
def login(user: UserLogin):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    db_user = cursor.fetchone()

    conn.close()

    if not db_user:
        return {"error": "Invalid username or password"}

    stored_password = db_user["password"]

    if not pwd_context.verify(user.password, stored_password):
        return {"error": "Invalid username or password"}

    return {
        "message": "Login successful",
        "username": db_user["username"]
    }

# =========================
# SAVE JOB (FIXED ROUTE)
# =========================
class SaveJobRequest(BaseModel):
    username: str
    job_id: str

@app.post("/save-job")
def save_job(data: SaveJobRequest):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    # Check if already saved
    cursor.execute(
        "SELECT * FROM saved_jobs WHERE username=? AND job_id=?",
        (data.username, data.job_id)
    )
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return {"message": "Job already saved"}

    cursor.execute(
        "INSERT INTO saved_jobs (username, job_id) VALUES (?, ?)",
        (data.username, data.job_id)
    )

    conn.commit()
    conn.close()

    return {"message": "Job saved successfully"}

# =========================
# GET MY SAVED JOBS (FIXED)
# =========================
@app.get("/my-jobs/{username}")
def get_my_jobs(username: str):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT jobs.*
        FROM jobs
        JOIN saved_jobs ON jobs.id = saved_jobs.job_id
        WHERE saved_jobs.username = ?
    """, (username,))

    rows = cursor.fetchall()
    conn.close()

    columns = ["id", "title", "company", "keyword", "url"]
    jobs = [dict(zip(columns, row)) for row in rows]

    return jobs