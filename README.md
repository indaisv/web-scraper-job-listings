# Job Listings Scraper

A Python scraper that collects job postings, structures them into a clean
dataset, and runs on a schedule — no manual re-running required.

## What it does

- Fetches job listings from a target site and parses each posting's title,
  company, location, date, and apply link
- Cleans the results into a pandas DataFrame and saves them to `jobs.csv`
- Runs automatically on a daily schedule, with error handling so a single
  failed run (site down, network issue) doesn't kill future runs
- Includes a separate Selenium demo for scraping JavaScript-rendered pages

## Why this exists

Static scraping (`requests` + `BeautifulSoup`) and JavaScript-rendered
scraping (`Selenium`) solve different problems. Real job boards use both
patterns depending on how they're built. This project demonstrates both,
plus the scheduling layer that turns a one-off script into something that
keeps a dataset current on its own.

## Tech stack

| Tool | Purpose |
|---|---|
| `requests` | HTTP requests to fetch page content |
| `BeautifulSoup4` (`lxml` parser) | Parse and extract data from static HTML |
| `Selenium` | Handle JavaScript-rendered pages |
| `pandas` | Structure scraped data, export to CSV |
| `schedule` | Run the scraper automatically on a recurring interval |
| `pytest` | Unit tests for the parsing logic |

## Project structure

```
web-scraper-job-listings/
├── src/
│   ├── scraper.py              # Main scraper: fetch, parse, save to CSV
│   ├── scheduler.py            # Wraps scraper.py to run on a daily schedule
│   └── day2_selenium_test.py   # Selenium demo for JS-rendered pages
├── data/
│   └── jobs.csv                # Scraped output
├── tests/
│   └── test_scraper.py         # Unit tests for parsing logic
├── requirements.txt
└── README.md
```

## Setup

```powershell
git clone https://github.com/indaisv/web-scraper-job-listings.git
cd web-scraper-job-listings
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

**Run the scraper once:**
```powershell
cd src
python scraper.py
```
Saves results to `jobs.csv` and prints a preview + row count.

**Run it on a schedule:**
```powershell
cd src
python scheduler.py
```
Runs once a day automatically. Leave the process running (or deploy it
somewhere that stays up) — it checks every second whether the scheduled
time has arrived, and logs a message on each successful (or failed) run.

**Run the Selenium demo:**
```powershell
cd src
python day2_selenium_test.py
```

## Running tests

```powershell
pytest
```

## Design notes

- The target site for the main pipeline renders job listings server-side,
  so `requests` + `BeautifulSoup` is sufficient and faster than spinning up
  a full browser — Selenium is used separately to demonstrate handling
  JS-rendered content, which many real job boards require.
- Scraping logic lives behind `if __name__ == "__main__":` in `scraper.py`,
  so `scheduler.py` can import and reuse `scrape_all_jobs()` without
  triggering a scrape on import.
- The scheduled job is wrapped in `try`/`except` — a failed scrape is
  logged, not fatal, so the scheduler keeps running and retries on the
  next scheduled interval.

## Possible next steps

- Swap `print()` logging for Python's `logging` module with timestamps
- Deploy the scheduler on a small always-on server or cron job instead of
  a long-running local process
- Add deduplication so re-runs don't overwrite history, just append new
  postings