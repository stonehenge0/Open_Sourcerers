from bs4 import BeautifulSoup
import requests
import csv


def extract_dzi_info(website):
    #  a function that extracts the info we want from the dzi pages. we repeatedly call it bc every page
    #  only has a few charities and we want the same kind of info from every page
    
    #  create list to store charity info
    charities_dzi = []
    # get div that contains all the charity info from the html script
    table = soup.find('div', attrs={"class": "e27posttypes e27posttypes-blocks blocks-3 bg-light"})

    #  for each charity extract relevant info (name, short description, link to DZI evaluation, where we get the rest of the info)
    for row in table.findAll('div',
                             attrs={'class': 'e27posttypes-block-item posttype-odaba'}):
        charity = {}
        name = row.find("div", attrs={"class": "e27posttypes-block-text"})
        charity["name"] = name.a.text
        charity["descript"] = name.p.text
        charity["eval_link"] = name.a["href"]
        charities_dzi.append(charity)

    return charities_dzi


#  setting the URL we want to get the data from
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/56.0.2924.76 Safari/537.36'}
URL_dzi = "https://www.dzi.de/organisation/"
s = requests.Session()

# only run if we can access the website
try:
    r = s.get(url=URL_dzi, headers=headers)
    if r.status_code != 200:
        raise ConnectionError
except ConnectionError:
    r = 0
    # print("No data received.")

if r:
    soup = BeautifulSoup(r.content, "html5lib")

    #  listing pages to be visited
    pages = []
    d = soup.find("div", class_="pagerdiv")
    for a in d.findAll("a", class_="page-numbers"):
        pages.append(a["href"])

    charity_list = extract_dzi_info(soup)

    #  going through all the pages of the website and extracting information
    for site in pages:
        p = s.get(url=site, headers=headers)
        new_soup = BeautifulSoup(p.content, "html5lib")
        for thing in extract_dzi_info(new_soup):
            charity_list.append(thing)

#  save the extracted info in a csv file
filename = 'dzi.csv'
with open(filename, 'w', newline='', encoding="UTF-8") as f:
    w = csv.DictWriter(f, ["name", "descript", "eval_link"])
    w.writeheader()
    for charity in charity_list:
        try:
            w.writerow(charity)
        except UnicodeEncodeError:
            continue
