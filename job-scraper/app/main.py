from uuid import uuid4
from passlib.context import CryptContext
from fastapi import FastAPI, Query, HTTPException, Depends
from pydantic import BaseModel
import sqlite3
from .models import UserCreate, UserLogin, Job
from .database import create_table, get_connection
from .scraper import scrape_jobs

app = FastAPI(title="Job Scraper API")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create base tables
create_table()


# INIT SAVED JOBS TABLE
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

# ROOT
@app.get("/")
def root():
    return {"message": "Job Scraper API is running"}


# SCRAPER
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


# GET ALL JOBS
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


# REGISTER
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
        "INSERT INTO users (id, username, password, role) VALUES (?, ?, ?, ?)",
        (user_id, user.username, hashed_password, "user")
    )


    conn.commit()
    conn.close()

    return {"message": "User registered successfully"}


# LOGIN
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

    if db_user["is_active"] == 0:
        return {"error": "Account is banned"}

    return {
        "message": "Login successful",
        "username": db_user["username"],
        "role": db_user["role"]
    }


# SAVE JOB
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


# GET MY SAVED JOBS
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

def get_current_user(username: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return dict(user)


def require_admin(username: str):
    user = get_current_user(username)

    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return user

@app.get("/admin/users")
def get_all_users(username: str, admin=Depends(require_admin)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, role FROM users")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

@app.get("/admin/saved-jobs")
def get_all_saved_jobs(username: str, admin=Depends(require_admin)):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM saved_jobs")
    rows = cursor.fetchall()
    conn.close()

    return rows

@app.delete("/admin/delete-user/{target_username}")
def delete_user(
    target_username: str,
    username: str,
    admin=Depends(require_admin)
):
    if target_username == username:
        raise HTTPException(status_code=400, detail="Admin cannot delete themselves")

    conn = get_connection()
    cursor = conn.cursor()

    # Delete user's saved jobs
    cursor.execute(
        "DELETE FROM saved_jobs WHERE username = ?",
        (target_username,)
    )

    # Delete user's scraped jobs
    cursor.execute("""
        DELETE FROM jobs
        WHERE user_id = (
            SELECT id FROM users WHERE username = ?
        )
    """, (target_username,))

    # Delete user
    cursor.execute(
        "DELETE FROM users WHERE username = ?",
        (target_username,)
    )

    conn.commit()
    conn.close()

    return {"message": f"User '{target_username}' deleted successfully"}

@app.put("/admin/change-role/{target_username}")
def change_role(
    target_username: str,
    new_role: str,
    username: str,
    admin=Depends(require_admin)
):
    if new_role not in ["user", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET role = ? WHERE username = ?",
        (new_role, target_username)
    )

    conn.commit()
    conn.close()

    return {"message": f"{target_username} is now {new_role}"}

@app.delete("/admin/delete-saved/{saved_id}")
def delete_saved_job(
    saved_id: int,
    username: str,
    admin=Depends(require_admin)
):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM saved_jobs WHERE id = ?",
        (saved_id,)
    )

    conn.commit()
    conn.close()

    return {"message": "Saved job deleted"}

@app.put("/admin/ban-user/{target_username}")
def ban_user(
    target_username: str,
    username: str,
    admin=Depends(require_admin)
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT is_active FROM users WHERE username = ?", (target_username,))
    user = cursor.fetchone()

    new_status = 0 if user["is_active"] == 1 else 1

    cursor.execute(
        "UPDATE users SET is_active = ? WHERE username = ?",
        (new_status, target_username)
    )

    conn.commit()
    conn.close()

    return {"message": f"{target_username} has been banned"}


@app.get("/admin/job-activity")
def job_activity(username: str, admin=Depends(require_admin)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT jobs.title, jobs.company, users.username, jobs.created_at
        FROM jobs
        JOIN users ON jobs.user_id = users.id
        ORDER BY jobs.created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


@app.get("/admin/saved-activity")
def saved_activity(username: str, admin=Depends(require_admin)):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT saved_jobs.id, saved_jobs.username, jobs.title, jobs.company
        FROM saved_jobs
        JOIN jobs ON saved_jobs.job_id = jobs.id
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows