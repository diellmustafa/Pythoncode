from fastapi import FastAPI
from .database import create_table, get_connection
from .scraper import scrape_jobs
from .models import Job

app = FastAPI(title="Job Scraper API")

create_table()

@app.get("/")
def root():
    return {"message": "Job Scraper API is running"}


@app.post("/scrape/{keyword}")
def run_scraper(keyword: str):
    jobs = scrape_jobs(keyword)
    return {"scraped_jobs": len(jobs)}


@app.get("/jobs", response_model=list[Job])
def get_jobs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]