from bs4 import BeautifulSoup
import requests
import csv


def extract_dzi_info(dzi_page):
    """Function takes html(str) and looks for relevant data (name, description, evaluation page link), returns list"""
    charities_dzi = []
    # All charities on a page are contained in this div.
    table_of_charities = dzi_page.find('div', attrs={"class": "e27posttypes e27posttypes-blocks blocks-3 bg-light"})

    # For each charity find its div and collect the relevant data.
    for charity_container in table_of_charities.findAll('div',
                                                        attrs={'class': 'e27posttypes-block-item posttype-odaba'}):
        charity = {}
        name = charity_container.find("div", attrs={"class": "e27posttypes-block-text"})
        charity["name"] = name.a.text
        charity["descript"] = name.p.text
        charity["eval_link"] = name.a["href"]
        charities_dzi.append(charity)

    return charities_dzi


#  Setting URL to scrape, getting html data and saving it as BeautifulSoup object
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/56.0.2924.76 Safari/537.36'}
#  Initiating URL and requests session
URL_dzi = "https://www.dzi.de/organisation/"
with requests.Session() as s:
    r = s.get(url=URL_dzi, headers=headers)
soup = BeautifulSoup(r.content, "html5lib")

# Listing pages to be visited (looks on page 1, starts list with page 2).
pages = []
d = soup.find("div", class_="pagerdiv")
for a in d.findAll("a", class_="page-numbers"):
    pages.append(a["href"])
# Collect all charities listed on page 1.
charity_list = extract_dzi_info(soup)

# Collect charity data from subsequent pages.
for site in pages:
    p = s.get(url=site, headers=headers)
    new_soup = BeautifulSoup(p.content, "html5lib")
    for charity_dict in extract_dzi_info(new_soup):
        charity_list.append(charity_dict)

#  Save the extracted charity data in csv file.
filename = 'dzi_01.csv'
with open(filename, 'w', newline='', encoding="UTF-8") as f:
    w = csv.DictWriter(f, ["name", "descript", "eval_link"])
    w.writeheader()
    for charity_data in charity_list:
        try:
            w.writerow(charity_data)
        except UnicodeEncodeError:
            continue
