
# Webscraping libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Utility libraries
import re
from datetime import date, timedelta
import time

# Data manipulation libraries
import pandas as pd

# Global variables
search_field_term_job = "data scientist"
search_field_term_location = "New York, NY"


# Load page with search results(job postings)
# define driver
driver = webdriver.Chrome()

# open url
driver.get("https://www.simplyhired.com/")

# wait for the page to load
driver.implicitly_wait(5)


# find and click on search field location
search_field = driver.find_element(By.XPATH, '//*[@id="field-:R5bakt9fbqm:"]')
search_field.click()

# clear search field
search_field.send_keys(Keys.CONTROL + "a")
search_field.send_keys(Keys.DELETE)

# enter search term job
search_field.send_keys(search_field_term_location)


# find and click on search field job
search_field = driver.find_element(By.XPATH, '//*[@id="field-:R3bakt9fbqm:"]')
search_field.click()

# wait for the page to load
driver.implicitly_wait(5)

# enter search term job
search_field.send_keys(search_field_term_job)
element = driver.switch_to.active_element
element.send_keys(Keys.ESCAPE)

# wait for the page to load
driver.implicitly_wait(5)


# submit form
search_field.send_keys(Keys.ENTER)


# set for jobs posted in the past 24 hours
driver.find_element(By.XPATH, '//*[@id="menu-button-:rl:"]').click()
time.sleep(2)
driver.find_elements(By.XPATH, '//*[@id="menu-list-:rl:"]//button')[1].click()