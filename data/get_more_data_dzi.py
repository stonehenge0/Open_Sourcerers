from bs4 import BeautifulSoup
import os
import pandas as pd
import requests

# Read in current state of dzi data file and establish requests session.
script_dir = os.path.dirname(__file__)
data_filename = "\\dzi.csv"
data_path = script_dir+data_filename

data = pd.read_csv(data_path)
links = data.loc[:]["eval_link"]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/56.0.2924.76 Safari/537.36'}
s = requests.Session()
# Keep track of runs, to match new and old data later.
run = 0

# Iterate through list of links to individual charity evaluation pages.
for link in links:
    URL = link
    r = s.get(url=URL, headers=headers)
    # If a link doesn't work, skip to the next one, but keep track of what charity we are on. 
    try:
        if r.status_code != 200:
            raise ConnectionError
    except ConnectionError:
        run += 1
        continue
    # Get html skript of page, navigate to relevant div.
    soup = BeautifulSoup(r.content, features="html5lib")
    div_all = soup.find("div", class_="odaba")
    div_main = div_all.find("div", class_="odabamain")
    # Dictionary for storing charity data.
    cherrytea = {}
    # Collect data on topics the charity works on (website is in german). 
    arbeitsschwerpunkte = div_main.find("h3", string="Arbeitsschwerpunkte")
    if arbeitsschwerpunkte:
        thema = arbeitsschwerpunkte.findNext("p")
        cherrytea["topic"] = thema.text.split(", ")
    else:
        cherrytea["topic"] = []
    # Collect data on countries the charity works in.
    land = div_main.find("h3", string="Länderschwerpunkte")
    if land:
        ort = land.findNext("p")
        cherrytea["countries"] = ort.text.split(", ")
    else:
        cherrytea["countries"] = []
    '''
    # collect revenue data of availabe
    money = div_main.find("th", string="Gesamteinnahmen:")
    if money:
        cherrytea["revenue"] = money.findNext("td").text.strip(" \n")
    else:
        cherrytea["revenue"] = str(0)

    accounting = div_main.find("a", href="/?p=2823")
    # collect money spend on bureaucracy if availabe
    if accounting:
        cherrytea["bureaucracy"] = accounting.findNext("td").text
    else:
        cherrytea["bureaucracy"] = str()
    '''
    recommendation_tx = div_main.find("a", href="/?p=2833")
    # Collect data on how DZI rates the charity's effectiveness 
    # and whether it is actively endorsed (from charity description text).
    if recommendation_tx:
        cherrytea["evaluation_textbased"] = recommendation_tx.findNext("p").text.split("\n")[0]
    else:
        cherrytea["evaluation_textbased"] = None
    # Collect data on how DZI rates the charity's effectiveness and whether it is actively endorsed ('warning' tag).
    recommendation_tag = div_main.find("span", class_="warnung")
    if recommendation_tag:
        cherrytea["evaluation_tag"] = recommendation_tag.text
    else:
        cherrytea["evaluation_tag"] = None

    web_site = div_all.find("strong", string="Website")
    # Store link to charity website if availabe. 
    if web_site:
        cherrytea["website"] = web_site.findNext("a")["href"]
    else:
        cherrytea["website"] = str()

    # Combine new and old data for each charity and store it in pandas.Dataframe, then save in csv file. 
    dictionary = dict(data.loc[run]) | cherrytea
    to_append = pd.DataFrame([dictionary])
    if not run:
        to_append.to_csv("dzi_more_info.csv", mode='w', index=False, header=True)
    else:
        to_append.to_csv("dzi_more_info.csv", mode='a', index=False, header=False)
    run += 1

s.close()
