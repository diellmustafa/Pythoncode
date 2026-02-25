import requests
from bs4 import BeautifulSoup
from uuid import uuid4
from .database import get_connection


def scrape_jobs(keyword: str, user_id: str):
    url = "https://realpython.github.io/fake-jobs/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    job_cards = soup.find_all("div", class_="card-content")

    conn = get_connection()
    cursor = conn.cursor()
    jobs = []

    for job in job_cards:
        title = job.find("h2", class_="title")
        company = job.find("h3", class_="company")
        location = job.find("p", class_="location")

        if not title or not company or not location:
            continue

        title_text = title.get_text(strip=True)
        company_text = company.get_text(strip=True)
        location_text = location.get_text(strip=True)

        # Filter by keyword
        if keyword.lower() not in title_text.lower():
            continue

        job_id = str(uuid4())

        cursor.execute(
            """
            INSERT INTO jobs (id, title, company, location, keyword, user_id)
VALUES (?, ?, ?, ?, ?, ?)
            """,
            (job_id, title_text, company_text, location_text, keyword, user_id),
        )

        jobs.append({
            "id": job_id,
            "title": title_text,
            "company": company_text,
            "location": location_text,
            "keyword": keyword,
            "user_id": user_id #temp
        })

    conn.commit()
    conn.close()

    print(f"Scraped {len(jobs)} jobs")
    return jobs