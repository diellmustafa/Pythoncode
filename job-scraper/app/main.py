from uuid import uuid4
from passlib.context import CryptContext
from .models import UserCreate, UserLogin
from fastapi import FastAPI, Query
from .database import create_table, get_connection
from .scraper import scrape_jobs
from .models import Job

app = FastAPI(title="Job Scraper API")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

create_table()

@app.get("/")
def root():
    return {"message": "Job Scraper API is running"}


@app.post("/scrape/{keyword}")
def scrape(keyword: str, username: str = Query(...)):
    conn = get_connection()
    cursor = conn.cursor()

    # Get user from DB
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    db_user = cursor.fetchone()

    if not db_user:
        conn.close()
        return {"error": "User not found"}

    user_id = db_user["id"] if isinstance(db_user, dict) else db_user[0]
    conn.close()

    jobs = scrape_jobs(keyword, user_id)
    return {"scraped_jobs": len(jobs)}


@app.get("/jobs", response_model=list[Job])
def get_jobs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

@app.post("/register")
def register(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return {"error": "Username already exists"}

    # Hash password
    hashed_password = pwd_context.hash(user.password)

    user_id = str(uuid4())

    cursor.execute(
        "INSERT INTO users (id, username, password) VALUES (?, ?, ?)",
        (user_id, user.username, hashed_password)
    )

    conn.commit()
    conn.close()

    return {"message": "User registered successfully"}

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

    # Verify password
    if not pwd_context.verify(user.password, stored_password):
        return {"error": "Invalid username or password"}

    return {
        "message": "Login successful",
        "username": db_user["username"]
    }

@app.get("/my-jobs")
def get_my_jobs(username: str):
    conn = get_connection()
    cursor = conn.cursor()

    # Get user
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    db_user = cursor.fetchone()

    if not db_user:
        conn.close()
        return {"error": "User not found"}

    user_id = db_user["id"] if isinstance(db_user, dict) else db_user[0]

    # Fetch only that user's jobs
    cursor.execute("SELECT * FROM jobs WHERE user_id = ?", (user_id,))
    jobs = cursor.fetchall()

    conn.close()
    return jobs