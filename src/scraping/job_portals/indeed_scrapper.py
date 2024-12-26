import requests
from bs4 import BeautifulSoup
from scraping.utils import save_to_database

def scrape_indeed_jobs(keyword, location, max_pages=5):
    base_url = "https://www.indeed.com/jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    jobs = []

    for page in range(max_pages):
        params = {
            "q": keyword,
            "l": location,
            "start": page * 10,
        }
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch page {page + 1}. Status Code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        for job_card in soup.select('.result'):
            try:
                title = job_card.select_one('h2.jobTitle').text.strip()
                company = job_card.select_one('.companyName').text.strip()
                loc = job_card.select_one('.companyLocation').text.strip()
                jobs.append({
                    "title": title,
                    "company": company,
                    "location": loc,
                })
            except AttributeError:
                continue

    save_to_database("indeed_jobs", jobs)
    print(f"Saved {len(jobs)} Indeed jobs to the database.")
    return jobs

if __name__ == "__main__":
    scrape_indeed_jobs("Data Scientist", "New York, NY")
