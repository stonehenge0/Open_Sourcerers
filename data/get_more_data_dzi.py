from bs4 import BeautifulSoup
import requests
import pandas as pd

data = pd.read_csv("dzi.csv")
links = data.loc[:]["eval_link"]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/56.0.2924.76 Safari/537.36'}
s = requests.Session()
run = 0

for link in links:
    URL = link
    r = s.get(url=URL, headers=headers)
    some_value = 0
    try:
        if r.status_code != 200:
            raise ConnectionError
    except ConnectionError:
        some_value = -1
        continue

    soup = BeautifulSoup(r.content, features="html5lib")
    div_all = soup.find("div", class_="odaba")
    div_main = div_all.find("div", class_="odabamain")
    
    cherrytea = {}

    arbeitsschwerpunkte = div_main.find("h3", string="Arbeitsschwerpunkte")
    if arbeitsschwerpunkte:
        thema = arbeitsschwerpunkte.findNext("p")
        cherrytea["topic"] = thema.text.split(", ")
    else:
        cherrytea["topic"] = []
    
    land = div_main.find("h3", string="Länderschwerpunkte")
    if land:
        ort = land.findNext("p")
        cherrytea["countries"] = ort.text.split(", ")
    else:
        cherrytea["countries"] = []

    money = div_main.find("th", string="Gesamteinnahmen:")
    if money:
        cherrytea["revenue"] = money.findNext("td").text.strip(" \n")
    else:
        cherrytea["revenue"] = str(0)

    accounting = div_main.find("a", href="/?p=2823")
    if accounting:
        cherrytea["bureaucracy"] = accounting.findNext("td").text
    else:
        cherrytea["bureaucracy"] = str()

    recommendation = div_main.find("a", href="/?p=2833")
    if recommendation:
        cherrytea["evaluation"] = recommendation.findNext("p").text.split("\n")[0]
    else:
        recommendation = div_main.find("span", class_="warnung")
        if recommendation:
            cherrytea["evaluation"] = recommendation.text
        else:
            cherrytea["evaluation"] = "No data"

    web_site = div_all.find("strong", string="Website")
    if web_site:
        cherrytea["website"] = web_site.findNext("a")["href"]
    else:
        cherrytea["website"] = str()

    dictionary = dict(data.loc[run]) | cherrytea
    to_append = pd.DataFrame([dictionary])
    if not run:
        to_append.to_csv("dzi_more_info.csv", mode='w', index=False, header=True)
    else:
        to_append.to_csv("dzi_more_info.csv", mode='a', index=False, header=False)
    run += 1

s.close()
