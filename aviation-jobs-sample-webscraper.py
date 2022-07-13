import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract(page):
  headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
  url = f'https://ph.indeed.com/jobs?q=aviation&l=philippines&start={page}'
  r = requests.get(url, headers)
  soup = BeautifulSoup(r.content, 'html.parser')
  return soup

def transform(soup):
  divs = soup.find_all('div', class_ = 'job_seen_beacon')
  for item in divs:
    title = item.find('span').text.strip()
    company = item.find('span', class_ = 'companyName').text.strip()
    location = item.find('div', class_ = 'companyLocation').text.strip()
    date = item.find('span', class_ = 'date').text.strip()
    try:
      salary = item.find('div', class_ = 'attribute_snippet').text.strip()
    except:
      salary = "None provided"

    job = {
      'title': title,
      'company': company,
      'location': location,
      'date': date,
      'salary': salary
    }    
    job_list.append(job)
  return

job_list = []

for i in range(0,40,10):
  print(f'Getting page, {i}')
  c = extract(0)
  transform(c)

df = pd.DataFrame(job_list)
# df.to_csv('jobs.csv')