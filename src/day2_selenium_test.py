"""
Selenium capability demo — separate from the main pipeline.
scraper.py handles the actual job-listing scrape via requests + BeautifulSoup,
since the target site renders server-side and doesn't need a browser.
This file demonstrates JS-rendered page handling with Selenium instead.
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()
driver.get("https://realpython.github.io/fake-jobs/")
time.sleep(5)  # Wait for the page to load

html = driver.page_source # Get the HTML source of the page

soup = BeautifulSoup(html, 'html.parser') # Parse the HTML with BeautifulSoup
print(soup.find('h1').text) # Print the text of the first h1 element
driver.quit() # Close the browser