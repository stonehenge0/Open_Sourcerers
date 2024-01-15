from bs4 import BeautifulSoup
import requests
import csv

#  setting the URL to scrape, getting the html info and saving it as BeautifulSoup obj
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/56.0.2924.76 Safari/537.36'}

URL_dzi = "https://www.dzi.de/organisation/"
URL_animals = "https://animalcharityevaluators.org/donation-advice/recommended-charities/"

#  cloudflare blocked (403)
#  URL_navigator = "https://www.charitynavigator.org/discover-charities/best-charities/"
#  URL_charity_watch = "https://www.charitywatch.org/top-rated-charities"

s = requests.Session()
try:
    r = s.get(url=URL_animals, headers=headers)
    if r.status_code != 200:
        raise ConnectionError
except ConnectionError:
    r = 0
    print("No data received.")

if r:
    soup = BeautifulSoup(r.content, "html5lib")
    #  create list to store charity info
    charities = []

    table = soup.find('div', attrs={"id":"grid"})

    #  for each charity extract relevant info
    for row in table.findAll('div', 
                             attrs={'class': 'card-detail-wrapper'}):
        charity = {}
        charity["name"] = row.h2.text
        charity["topic"] = []
        for tag in row.findAll("i"):
            charity["topic"].append(tag["title"])
        charity["eval_link"] = row.a["href"]
        charities.append(charity)

    #  save the extracted info in a csv file
    filename = 'animalcharities.csv'
    with open(filename, 'w', newline='', encoding="UTF-8") as f:
        w = csv.DictWriter(f, ["name", "topic", "eval_link"])
        w.writeheader()
        for charity in charities:
            try:
                w.writerow(charity)
            except UnicodeEncodeError:
                continue
