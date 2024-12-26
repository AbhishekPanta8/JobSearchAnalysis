import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LINKEDIN_COOKIE = os.getenv("LINKEDIN_COOKIE")


def scrape_linkedin_jobs(keyword, location, max_pages=5):
    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.64 Safari/537.36",
        "Cookie": LINKEDIN_COOKIE,
    }
    jobs = []

    for page in range(max_pages):
        try:
            # Parameters for the search request
            params = {
                "keywords": keyword,
                "location": location,
                "start": page * 25,
            }

            # Fetch the page
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()  # Raise an HTTPError if the status is 4xx or 5xx

            # Parse the HTML response
            soup = BeautifulSoup(response.text, "html.parser")
            job_cards = soup.select('.base-card')

            if not job_cards:
                print(f"No jobs found on page {page + 1}.")
                break

            for job_card in job_cards:
                try:
                    title = job_card.select_one('.base-card__title').text.strip() if job_card.select_one('.base-card__title') else "N/A"
                    company = job_card.select_one('.base-card__subtitle').text.strip() if job_card.select_one('.base-card__subtitle') else "N/A"
                    loc = job_card.select_one('.job-card-container__metadata-item').text.strip() if job_card.select_one('.job-card-container__metadata-item') else "N/A"
                    link = job_card.select_one('.base-card__full-link')['href'] if job_card.select_one('.base-card__full-link') else "N/A"

                    # Append job details to the list
                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": loc,
                        "link": link,
                    })
                except Exception as e:
                    print(f"Error processing a job card: {e}")

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch page {page + 1}: {e}")

    # Save jobs to a file
    save_jobs_to_file(jobs)
    print(f"Saved {len(jobs)} LinkedIn jobs to data/linkedin_jobs.json")
    return jobs


def save_jobs_to_file(jobs):
    """Save scraped jobs to a JSON file."""
    import json
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", "linkedin_jobs.json")
    try:
        with open(file_path, "w") as file:
            json.dump(jobs, file, indent=4)
        print(f"Jobs saved successfully to {file_path}.")
    except Exception as e:
        print(f"Failed to save jobs to file: {e}")


if __name__ == "__main__":
    scrape_linkedin_jobs("Software Engineer", "San Francisco, CA")
