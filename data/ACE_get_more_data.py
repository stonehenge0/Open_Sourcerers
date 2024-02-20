from bs4 import BeautifulSoup
import os
import pandas as pd
import requests

# Setting up the path to current state of data file. 
script_dir = os.path.dirname(__file__)
data_filename = "\\ACE_data_01.csv"
data_path = script_dir+data_filename

data = pd.read_csv(data_path)
links = data.loc[:]["eval_link"]

# Since pycountry didn't recognize abbrevitions and some country names, I included another list.
world_countries = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola',
                   'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia',
                   'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium',
                   'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia', 'Bosnia and Herzegovina', 'Botswana',
                   'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria',
                   'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands',
                   'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands',
                   'Colombia', 'Comoros', 'Congo', 'Democratic Republic of the Congo', 'Cook Islands', 'Costa Rica',
                   "Côte d'Ivoire", "Cote d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic',
                   'Denmark', 'Djibouti', 'Dominica ', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador',
                   'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands', 'Faroe Islands', 'Fiji',
                   'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon',
                   'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe',
                   'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guinea Bissau', 'Guyana', 'Haiti',
                   'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Vatican', 'Honduras',
                   'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle of Man',
                   'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati',
                   "Democratic People's Republic of Korea", 'North Korea', 'South Korea', 'Kuwait', "North Ireland"
                   'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya',
                   'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia', 'North Macedonia', 'Madagascar',
                   'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania',
                   'Mauritius', 'Mayotte', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro',
                   'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands',
                   'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Norway',
                   'Northern Mariana Islands', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory', 'Palestine',
                   'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal',
                   'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russia', 'Russian Federation', 'Rwanda',
                   'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis',
                   'Saint Lucia', 'Saint Martin', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines',
                   'Samoa', 'San Marino', 'Sao Tome', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia',
                   'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten', 'Slovakia', 'Slovenia', 'Solomon Islands',
                   'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka',
                   'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland',
                   'Syrian Arab Republic', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste',
                   'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan',
                   'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom',
                   'U.K.', 'UK', 'Great Britain', 'England', 'Scottland', 'Wales', 'USA', 'United States', 'U.S.',
                   'U. S.', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Virgin Islands',
                   'Virgin Islands', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/56.0.2924.76 Safari/537.36'}
s = requests.Session()
run = 0
spreadsheets = []
# Go through the individual evaluation pages for each charity, where detailed information is found.
for link in links:
    URL = link
    r = s.get(url=URL, headers=headers)
    some_value = 0
    try:
        if r.status_code != 200:
            raise ConnectionError
    except ConnectionError:
        some_value = -1
        run += 1
        continue

    # Store information on charity website and description.
    cherrytea = {}
    soup = BeautifulSoup(r.content, "html5lib")
    cherrytea["website"] = soup.find("span", string="Website").findNext("a")["href"]
    cherrytea["description"] = soup.find("span",
                                         class_="single-review-charity-status").findNext("p").findNext("p").text

    # Find country info in website text, if available, if not look in project description for countries. 
    country_info = soup.find("h4", string="Countries")
    countries_found = set()
    if country_info:
        country_text_list = [country_info.findNext("p"), country_info.findNext("p").findNext("p")]
        country_text = ("".join([str(i) for i in country_text_list[0]]) + " "
                        + "".join([str(i) for i in country_text_list[1]]))
        # If a country is mentioned in the countries section, add it to list of countries the charity operates in.
        for state in world_countries:
            if state in country_text:
                # Some states appear multiple times in the list of countries, they all should produce the same lable. 
                if state == "U.S." or state == "U. S." or state == "USA":
                    countries_found.add("United States")
                elif state == "Democratic People's Republic of Korea":
                    countries_found.add("North Korea")
                elif state == "Syrian Arab Republic":
                    countries_found.add("Syria")
                elif (state == "U.K." or state == "Great Britain" or state == "UK" or state == "England"
                      or state == "Scottland" or state == "Wales" or state == "North Ireland"):
                    countries_found.add("United Kingdom")
                else:
                    countries_found.add(state)
    else:
        # For charities without country details, the information sometimes appears in the description of the charity.
        for state in world_countries:
            if state in cherrytea["description"]:
                if state == "U.S." or state == "U. S." or state == "USA":
                    countries_found.add("United States")
                elif state == "Democratic People's Republic of Korea":
                    countries_found.add("North Korea")
                elif state == "Syrian Arab Republic":
                    countries_found.add("South Korea")
                elif state == "U.K." or state == "Great Britain" or state == "UK":
                    countries_found.add("United Kingdom")
                elif state == "England" or state == "Scottland" or state == "Wales" or state == "North Ireland":
                    countries_found.add("United Kingdom")
                else:
                    countries_found.add(state)
    if countries_found:
        cherrytea["country_info"] = list(countries_found)
    # In case there is no country information, set the charity to global. 
    else:
        cherrytea["country_info"] = ["global"]

    # Find effectiveness score in cost-effectiveness evaluation text. 
    cost_effectiveness_container = soup.find("h2", id="c2")
    # Navigate to "Our Assessment" headline, which has the efficiency score in the first sentence (if available).
    if cost_effectiveness_container:
        cost_effectiveness_text = cost_effectiveness_container.findNext("h3")
        score = 0
        while score < 10:
            if "Our Assessment" in cost_effectiveness_text.text:
                effectiveness_text = cost_effectiveness_text.findNext("p").text
                effectiveness_rating = [char for char in effectiveness_text if char.isdigit()]
                cherrytea["effectiveness"] = ".".join([effectiveness_rating[0], effectiveness_rating[1]])
                score = 99
            else:
                cost_effectiveness_text = cost_effectiveness_text.findNext("h3")
                cherrytea["effectiveness"] = "0"
                score += 1
    else:
        cherrytea["effectiveness"] = "0"
        # There are spreadsheets that have the effectiveness scores if they are not listed on the webpage itself
        # The spreadsheets could be used for getting additional data in the future if needed
        if soup.find("a", string="Cost-Effectiveness spreadsheet"):
            spreadsheet_link = soup.find("a", string="Cost-Effectiveness spreadsheet")["href"]
            spreadsheets.append([data.loc[run]["name"], spreadsheet_link])
        elif soup.find("a", string="Cost Effectiveness spreadsheet"):
            spreadsheet_link = soup.find("a", string="Cost Effectiveness spreadsheet")["href"]
            spreadsheets.append([data.loc[run]["name"], spreadsheet_link])
        else:
            spreadsheet_link = ""

    dictionary = dict(data.loc[run]) | cherrytea
    to_append = pd.DataFrame([dictionary])
    if not run:
        to_append.to_excel("ACE_more_info.xlsx", index=False, header=True)
    else:
        with pd.ExcelWriter('ACE_more_info.xlsx', mode='a', if_sheet_exists='overlay') as writer:
            to_append.to_excel(writer, index=False, header=False, startrow=run+1)
    run += 1
