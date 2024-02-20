import numpy as np
import os
import pandas as pd
import pycountry
import pycountry_convert as pc
from googletrans import Translator


# Datatype Cleanup Functions


def empty_list_to_nan(lst):
    """ Takes empty list and returns numpy.nan, if list isn't empty returns original list. """
    if lst[0] == "":
        return np.nan
    else:
        return lst


def str_to_list(string):
    """ Function takes string, strips if of "[", "]" and "'", then returns it as a list. """
    return string.strip("[']").split("', '")


# Loading current version of the dataset
script_dir = os.path.dirname(__file__)
data_filename = "\\dzi_more_info.csv"
data_path = script_dir+data_filename
DZI_data = pd.read_csv(data_path)

# Drop any rows, that have no efficiency data or no website we can later link to.
DZI_data = DZI_data.dropna(subset=["evaluation_textbased", "evaluation_tag"], how="all")
DZI_data = DZI_data.dropna(subset=["website"])
# Correcting data type.
DZI_data["countries"] = DZI_data["countries"].map(str_to_list)
DZI_data["topic"] = DZI_data["topic"].map(str_to_list)

# Turn empty country and category lists into NaN values and remove charities missing data in multiple columns.
DZI_data.countries = DZI_data.countries.apply(empty_list_to_nan)
DZI_data.topic = DZI_data.topic.apply(empty_list_to_nan)
DZI_data = DZI_data.dropna(subset=["countries", "topic"], how="all")
# Drop rows missing data and fill remaining NaN values with empty strings.
DZI_data.countries = DZI_data.countries.fillna(value="")
DZI_data.topic = DZI_data.topic.fillna(value="")
DZI_data.evaluation_textbased = DZI_data.evaluation_textbased.fillna(value="")
DZI_data.evaluation_tag = DZI_data.evaluation_tag.fillna(value="")

# Drop charities DZI explicitly advises against, since those shouldn't be recommended.
# "DZI-Spenderberatung warnt" = "DZI donor consultation is warning against"
# "nicht förderungswürdig" = "not worthy of support"
DZI_data = DZI_data[~(DZI_data.evaluation_tag.str.contains("DZI-Spenderberatung warnt")
                      | DZI_data.evaluation_tag.str.contains("nicht förderungswürdig"))]


# Efficiency Rating


def dzi_efficency_scorer(row):
    """ Function takes a pd.Series and returns an int 1,2 or 3 based on the content of the evaluation_tag 
    and evaluation_textbased columns data, returns none if no relevant content is found.
    """
    if "Einschätzung nicht möglich" in row.evaluation_tag:
        return 1
    elif "neutral" in row.evaluation_tag:
        return 2
    elif ("DZI Spenden-Siegel zuerkannt" in row.evaluation_textbased
          or "ist förderungswürdig" in row.evaluation_textbased):
        return 3
    else:
        return None


# Add new column 'efficiency_score'.
# Lack of efficiency data: 1
# Not actively endorsed/neutral: 2
# 3 awarded to actively supported charites.
# Since DZI data doesn't give enough detail to differenciate top efficiency charities, 4 cannot be awarded.

DZI_data["efficiency_score"] = DZI_data.apply(dzi_efficency_scorer, axis=1)
# Remove rows, where no efficiency score could be calculated
DZI_data = DZI_data.dropna(subset=["efficiency_score"])


# Country and Continent Tags


def country_to_continent(countries):
    """Input: list of country names
    Output: continent name (or 'global')
    Function converts country name to continent name by converting to their ISO numbers and back.
    Special cases for countries pycountry doesn't recognize. """
    continent_s = set()
    for country_name in countries:
        if country_name == "global":
            continent_s = set("global")
            break
        else:
            try:
                country_alpha2 = pc.country_name_to_country_alpha2(country_name)
                country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
                country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
                continent_s.add(country_continent_name)
            except KeyError:
                if country_name == "Kosovo":
                    continent_s.add("Europe")
                elif country_name == "Tibet" or country_name == "Timor-Leste":
                    continent_s.add("Asia")
                elif country_name == "Western Sahara":
                    continent_s.add("Africa")
                else:
                    pass
    if len(continent_s) > 2:
        return ["global"]
    else:
        return list(continent_s)


def english_country_name(german_names):
    """Takes a list of strings, translates each string (ger-eng) and returns the translated list. """
    english_countries = []
    for name in german_names:
        if name in DZI_countries_de:
            english_countries.append(country_translation[name])
    return english_countries


def ger_to_eng(text):
    """ Function that uses Google Tranlsate API to translate German text to English. """
    translator = Translator()
    translation = translator.translate(text, src="de", dest="en")
    return translation.text


# Setting up a translation dictionary for all countries that appear in the data. 
DZI_countries_de = []
DZI_countries_en = []
for laender in DZI_data["countries"]:
    for land in laender:
        if land:
            if land not in DZI_countries_de:
                DZI_countries_de.append(land)
                DZI_countries_en.append(ger_to_eng(land))

# Make a country translation dictionary. Change some suboptimal translations. 
country_translation = dict(zip(DZI_countries_de, DZI_countries_en))
country_translation.update({"weltweit": "global", "Palästinensische Gebiete": "Palestine", "Togo": "Togo",
                            "Nordirland": "United Kingdom", "Äquatorialguinea": "Equatorial Guinea", "Gabun": "Gabon",
                            "Kirgistan": "Kyrgyzstan", "Dschibuti": "Djibouti", "Nordmazedonien": "North Macedonia",
                            "Demokratische Republik Kongo": "Democratic Republic of the Congo", "Botsuana": "Botswana",
                            "Côte d’Ivoire": "Ivory Coast", "Komoren": "Comoros", "Republik Korea": "South Korea",
                            "Salomonen": "Solomon Islands", "Cookinseln": "Cook Islands",
                            "Sao Tomé und Principe": "Sao Tome and Principe"})

DZI_data["countries_en"] = DZI_data["countries"].apply(english_country_name)
DZI_data["continent"] = DZI_data["countries_en"].apply(country_to_continent)


# Area/Topic of Work


def topic_to_category(initial_topic):
    """ Input: List
    Output: List
    Takes list of categories and matches them to broader categories based on dictionary key mappings. 
    """
    categories = set()
    for lable in initial_topic:
        if lable in category_dict:
            categories.add(category_dict[lable])
    return list(categories)


# Create list of (unique) areas of work mentioned in the DZI data. 
DZI_topics = []
for themen in DZI_data["topic"]:
    for thema in themen:
        if thema:
            if thema not in DZI_topics:
                DZI_topics.append(thema)

# Categories to match the original lables to. 
categorys = ["children, youth and family", "children, youth and family", "campaigning and educational work",
             "women's empowerment", "healthcare and prevention", "campaigning and educational work",
             "economic development", "environment and conservation", "refugees", "disaster relief", "disaster relief",
             "individual support", "culture and religion", "people with disabilities", "elderly", "human rights",
             "intercultural understanding", "culture and religion", "HIV/AIDS", "children, youth and family",
             "general animal welfare", "criminal offenders", "sports", "research", "emergency medical services",
             "addiction", "campaigning and educational work", "campaigning and educational work"]
# Matching original lables to our categories. 
category_dict = dict(zip(DZI_topics, categorys))

# Assign values to "subcategory" column
DZI_data["subcategory"] = DZI_data["topic"].apply(topic_to_category)

# None of the charities target x-crisis topics.
DZI_data.insert(3, "x-crisis", "n")

# All data is taken from dzi.de ("Deutsches Zentralinstitut für soziale Fragen").
DZI_data.insert(7, column="evaluator", value="DZI (german)")

DZI_to_keep = DZI_data.filter(items=["name", "subcategory", "x-crisis", "countries_en", "continent",
                                     "efficiency_score", "evaluator", "website", "eval_link"])
DZI_to_keep = DZI_to_keep.rename(columns={"efficiency_score": "efficiency", "subcategory": "category",
                                          "countries_en": "country", "eval_link": "evaluation"})
# Save final dataset
with pd.ExcelWriter('final_dzi.xlsx', mode='w') as writer:
    DZI_to_keep.to_excel(writer, index=False, header=True)

