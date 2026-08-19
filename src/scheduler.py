import schedule
import time
import pandas as pd
from scraper import scrape_all_jobs, URL 

def job():
    print("Running scheduled scrape....")
    try:
        jobs = scrape_all_jobs(URL)
        df = pd.DataFrame(jobs)
        df.to_csv("jobs.csv", index= False)
        print(f"Saved {len(df)} jobs to jobs.csv")
    except Exception as e:
        print(f"Scrape failed: {e}")
    
schedule.every().day.at("09:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)