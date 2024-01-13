from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import pandas as pd


import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring

def getJobDescription(link:str) -> str:
  """ Gets the job description of a role of the VentureLoop Website
  """
  if pd.isna(link):
    return pd.NA
  
  page = requests.get(link)

  # Extracts the response as html: html_doc
  html_doc = page.text

  # Create a BeautifulSoup object from the HTML: soup
  soup = BeautifulSoup(html_doc,features="lxml")

  dom = fromstring(str(soup))

  description = dom.xpath('//*[@id="formContainer"]/form/div/div/div[3]/div[2]')[0].text_content()

  return description



driver = webdriver.Chrome()

driver.get("https://www.ventureloop.com/ventureloop/home.php")

# watit for the page to load
driver.implicitly_wait(5)

# find and click on search field
search_field = driver.find_element(By.ID, "keywords")
search_field.click()

# enter search term and submit
search_field.send_keys("data scientist") #+Keys.RETURN)
# driver.implicitly_wait(5)
search_field.submit()

# Define empty lists to store the scraped data
job_list = []

# get number of pages
num_pages = len(driver.find_elements(By.XPATH,'//*[@id="formContainer"]/form/div[2]/div/div[2]/span'))

# get number of rows on first page
num_rows = len(driver.find_elements(By.XPATH, f'//*[@id="news_tbl"]/tbody/tr'))

# get number of columns
num_cols = len(driver.find_elements(By.XPATH, f'//*[@id="news_tbl"]/tbody/tr[1]/th'))

# Extract the job data
for i in range(2,num_rows):
    job_list.append([driver.find_element(By.XPATH, f'//*[@id="news_tbl"]/tbody/tr[position()={i}]/td[position()={j}]').text for j in range(1,num_cols +1)])
    
    # get links from first column with job describtion
    #link.append(driver.find_element(By.XPATH, f'//*[@id="news_tbl"]/tbody/tr[position()={i}]/td/a').get_attribute("href"))
    try:
        link = driver.find_element(By.XPATH, f'//*[@id="news_tbl"]/tbody/tr[position()={i}]/td/a').get_attribute("href")
        job_list[-1].append(link)
    except:
        job_list[-1].append(pd.NA)



# loop through pages
for p in range(2, num_pages +1):
    # click on page
    driver.find_element(By.XPATH,'//*[@id="formContainer"]/form/div[2]/div/div[2]/span[@class="nav current custnav pagnav"]/following-sibling::span/a').click()
    # watit for the page to load
    driver.implicitly_wait(5)
    # Extract the job data

    # get number of rows
    num_rows = len(driver.find_elements(By.XPATH, f'//*[@id="news_tbl"]/tbody/tr'))

    for i in range(2,num_rows):
        try:
            job_list.append([driver.find_element(By.XPATH,
                                                  f'//*[@id="news_tbl"]/tbody/tr[position()={i}]/td[position()={j}]').text for j in range(1,num_cols +1)])
        

            link = driver.find_element(By.XPATH, f'//*[@id="news_tbl"]/tbody/tr[position()={i}]/td/a').get_attribute("href")
            job_list[-1].append(link)
        except:
            print(f"Error at row {i} on page {p}")


# Store data 
jobs = pd.DataFrame(job_list)

# Set columns
cols = [driver.find_element(By.XPATH, f'//*[@id="news_tbl"]/tbody/tr[position()={1}]/th[position()={j}]').text for j in range(1,6)]
cols.append('link')
jobs.columns = cols


# add job description to dataframe
jobs["Job_description"] = jobs["link"].apply(getJobDescription)
jobs = jobs.drop_duplicates()

print(jobs.head())
print(jobs.shape)

jobs.to_csv('jobs.csv', index=False)

#driver.close()