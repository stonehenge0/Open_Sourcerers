from bs4 import BeautifulSoup
import requests
import csv

#  Setting the URL to scrape and initializing requests Session
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/56.0.2924.76 Safari/537.36'}
URL_dzi = "https://www.dzi.de/organisation/"
URL_animals = "https://animalcharityevaluators.org/donation-advice/recommended-charities/"
s = requests.Session()
# connecting to the website and storing the received data in r
try:
    r = s.get(url=URL_animals, headers=headers)
    if r.status_code != 200:
        raise ConnectionError
except ConnectionError:
    r = 0
    print("No data received.")
finally:
    charities = []
s.close()
if r:
    soup = BeautifulSoup(r.content, "html5lib")
    table = soup.find('div', attrs={"id": "grid"})
    #  for each charity extract relevant data
    for row in table.findAll('div',
                             attrs={'class': 'card-detail-wrapper'}):
        charity = {}
        charity["name"] = row.h2.text
        charity["topic"] = []
        for tag in row.findAll("i"):
            charity["topic"].append(tag["title"])
        if not charity["topic"]:
            charity["topic"] = None
        charity["eval_link"] = row.a["href"]
        charities.append(charity)

#  save the extracted info in a csv file for further use
filename = 'ACE_data_01.csv'
with open(filename, 'w', newline='', encoding="UTF-8") as f:
    w = csv.DictWriter(f, ["name", "topic", "eval_link"])
    w.writeheader()
    for charity in charities:
        try:
            w.writerow(charity)
        except UnicodeEncodeError:
            continue
