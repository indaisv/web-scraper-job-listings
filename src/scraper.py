import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://realpython.github.io/fake-jobs/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/58.0.3029.110 Safari/537.36"
    )
}


def fetch_soup(url: str) -> BeautifulSoup:
    """Fetch a page and return a parsed BeautifulSoup object."""
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "lxml")


def parse_job_card(card) -> dict:
    """Extract one job's information from a single job card."""

    title = card.find("h2", class_="title")
    company = card.find("h3", class_="company")
    location = card.find("p", class_="location")
    date = card.find("time")

    links = card.find_all("a")
    apply_link = links[1]["href"] if len(links) > 1 else "N/A"

    job = {
        "title": title.text.strip() if title else "N/A",
        "company": company.text.strip() if company else "N/A",
        "location": location.text.strip() if location else "N/A",
        "date": date.text.strip() if date else "N/A",
        "apply_link": apply_link,
    }

    return job


def scrape_all_jobs(url: str) -> list[dict]:
    """Fetch the page, parse all job cards, and return a list of dictionaries."""
    soup = fetch_soup(url)

    results_container = soup.find(id="ResultsContainer")

    if results_container is None:
        return []

    cards = results_container.find_all("div", class_="card-content")

    jobs = []
    for card in cards:
        jobs.append(parse_job_card(card))

    return jobs


if __name__ == "__main__":
    jobs = scrape_all_jobs(URL)

    df = pd.DataFrame(jobs)

    print(df.head())
    print(df.shape)

    df.to_csv("jobs.csv", index=False)
    print("\nJobs saved to jobs.csv")