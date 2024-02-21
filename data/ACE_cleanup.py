import numpy as np
import os
import pandas as pd
import pycountry
import pycountry_convert as pc


def country_to_continent(countries):
    """Input: list of country names
    Output: continent name (or global)
    This function converts a country name to a continent name by converting to their ISO numbers and back.
    """
    continent_s = set()
    for country_name in countries:
        try:
            country_alpha2 = pc.country_name_to_country_alpha2(country_name)
            country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
            country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
            continent_s.add(country_continent_name)
        except KeyError:
            pass
    if len(continent_s) > 2:
        return ["global"]
    else:
        return list(continent_s)


def map_to_categories(initial_categories):
    """Function takes the initial categories (list) and maps them onto broader categories, returns string
    returns category, if charity matches only one, then prioritizes from most to least specific
    """
    categories = set()
    for lable in initial_categories:
        if lable in topics_dict:
            categories.add(topics_dict[lable])
        else:
            categories.add("other")
    if len(categories) == 1:
        if "other" in categories:
            return "general animal welfare"
        else:
            return list(categories)[0]
    elif "nutrition and industrial livestock alternatives" in categories:
        return "nutrition and industrial livestock alternatives"
    elif "animal rights" in categories:
        return "animal rights"
    else:
        return "general animal welfare"


def str_to_list(string):
    """ Function turns a list that has been interpreted as a string (or any other string) back into a list """
    return string.strip("[']").split("', '")


script_dir = os.path.dirname(__file__)
data_filename = "\\ACE_more_info.xlsx"
data_path = script_dir+data_filename
ACE_data = pd.read_excel("data_path")

# Filling in missing "topic" data for one charity that is missing it.
# Can easily be looked up since it's only one missing value.

ACE_data.at[10, 'topic'] = "Cellular Agriculture"

# Turn ACE's efficiency rating into our general rating (2 exploratory, 3 promising, 4 top rate).
# Since ACE only lists charities they rate somewhat effective, all get assigned a value of at least 2. Charities
# initially rated zero are those without a rating listed on the ACE charity page, i.e. those not actively supported.
# Values higher than 4.0 (ACE) represent highly effective charities.

effect_conditions = [(ACE_data["effectiveness"] == 0), (ACE_data["effectiveness"] <= 4.0),
                     (ACE_data["effectiveness"] > 4.0)]
ACE_data["effectiveness_norm"] = np.select(effect_conditions, [2, 3, 4])

# Correct datatype.
ACE_data["topic"] = ACE_data["topic"].map(str_to_list)
ACE_data["country_info"] = ACE_data["country_info"].map(str_to_list)

### Find all mentioned categories the charities fall into. (not necessary anymore)
# animal_topics = []
# for lists in ACE_data["topic"]:
#    for element in lists:
#        animal_topics.append(element)
# animal_topics_list = np.unique(animal_topics).tolist()

topics_dict = {'Capacity Building': "animal rights",
               'Cellular Agriculture': "nutrition and industrial livestock alternatives",
               'Cultured and Plant-Based Food Tech': "nutrition and industrial livestock alternatives",
               'Fur Industry': "general animal welfare", 'General Animal Advocacy': "general animal welfare",
               'Industrial Agriculture': "general animal welfare", 'Legal and Legislative': "animal rights",
               'Reducing Wild Animal Suffering': "general animal welfare", 'Veterinary': "general animal welfare"}

# Add column with category tags to dataframe.
ACE_data["category_narrow"] = ACE_data["topic"].apply(map_to_categories)
# Make continent tags based on country_info column.
ACE_data["continent"] = ACE_data["country_info"].apply(country_to_continent)

# No animal charities target x-crisis topics.
ACE_data.insert(3, "x-crisis", "n")
# What charity evaluator did we take the data from: www.animalcharityevaluators.org (ACE)
ACE_data.insert(7, column="evaluator", value="ACE")

# Make a new dataframe of only the data we want to use for further steps and rename them
ACE_to_keep = ACE_data.filter(items=["name", "category_narrow", "x-crisis", "country_info", "continent",
                                     "effectiveness_norm", "evaluator", "website", "eval_link"])
ACE_to_keep = ACE_to_keep.rename(columns={"effectiveness_norm": "efficiency", "category_narrow": "category",
                                          "country_info": "country", "eval_link": "evaluation"})

with pd.ExcelWriter('final_ACE.xlsx', mode='w') as writer:
    ACE_to_keep.to_excel(writer, index=False, header=True)
