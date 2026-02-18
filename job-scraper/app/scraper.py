import requests
from bs4 import BeautifulSoup
from uuid import uuid4
from .database import get_connection


def scrape_jobs(keyword: str = "python"):
    url = f"https://remoteok.com/remote-{keyword}-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch jobs: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    listings = soup.find_all("tr", class_="job")

    if not listings:
        return []

    conn = get_connection()
    cursor = conn.cursor()

    jobs = []

    for job in listings:
        try:
            title_tag = job.find("h2")
            company_tag = job.find("h3")

            if not title_tag or not company_tag:
                continue

            job_id = str(uuid4())

            cursor.execute(
                "INSERT OR IGNORE INTO jobs (id, title, company, location, keyword) VALUES (?, ?, ?, ?, ?)",
                (job_id, title_tag.text.strip(), company_tag.text.strip(), "Remote", keyword)
            )

            jobs.append({
                "id": job_id,
                "title": title_tag.text.strip(),
                "company": company_tag.text.strip(),
                "location": "Remote",
                "keyword": keyword
            })

        except Exception as e:
            print("Skipping job due to error:", e)

    conn.commit()
    conn.close()

    return jobss