<br>
<br>
<a href="https://github.com/DenverCoder1/readme-typing-svg"><img src="https://readme-typing-svg.herokuapp.com?font=Time+New+Roman&color=cyan&size=25&center=true&vCenter=true&width=900&height=100&lines=Not+sure+what+charity+to+donate+to?;++We+can+help!++;Get+to+know+more+below..."></a>
<br>

<center>
<div style="width:100%;text-align:center;">
<img src='https://github.com/stonehenge0/Open_Sourcerers/blob/main/docs/static/Apfelkuchen.jpg' width="197" height="167">  
</div>
</center>


# Final presentation
https://docs.google.com/presentation/d/1W9WDpjblKqI7NbVhbs1zIHmNB68DqaqjX7LX9M4YqHg/edit?usp=sharing

---
## Charity Picker
The ApplePy Charity pickers helps you find a charity to donate to. Over our website, the user can enter their preferences and we will suggest charities from our database that most closely match what they are looking for. 

## Motivation
The motivation behind this project was to combine multiple sources and extend their original functionalities to have a database of searchable, topically diverse, and cost-effective charities.
Our sources consist of charity evaluators focusing on animal charities, charities with high cost-efficiency, longterm impact charities and a more broad evaluator. Since we sources our charities fom charity evaluators that have conducted in-depth research on their charities we ensure high quality recommendations. We also give the user the option to work with cost-efficiency scores, that measure how much positive impact a charity can have with a given sum of money. This too is information that was usually not directly available or not provided to begin with at all.    

## Features
- A database consisting of four different evaluators each focusing on different aspects of charitable giving. Their data has been extended to include links to the charities, geographic information, in-depth cost-effectiveness analyses and more. 
- An algorithm to match user preferences with the charities in our database and return close matches.
- Visualizations about our data sources and the results our algorithm produces.
- An easy to use website, so users without coding experience can acces our functionalities.


## Code examples
We first read in the data that we have from each of our sources, in this case using webscraping with [Beautiful soup](https://pypi.org/project/beautifulsoup4/).

> Note: the process of extracting, processing and scraping data varies strongly between our sources. In favour of simplicity, the data collection process will be shown at the example of ACE (Animal Charity Evaluator) here.

```sh
try:
    r = s.get(url=URL_animals, headers=headers)
if r:
    soup = BeautifulSoup(r.content, "html5lib")
    table = soup.find('div', attrs={"id": "grid"})
    #  for each charity extract relevant data
    for row in table.findAll('div',
                             attrs={'class': 'card-detail-wrapper'}):
        charity = {}
        charity["name"] = row.h2.text
        charity["eval_link"] = row.a["href"]
        # ...
```
> Most of the code/functions here were shortened for the purpose of readability, you can find the full functions in the respective folders.


After extracting the data, we see what the data is missing to fit in our scheme: In this case ACE did not specify the continents that a charity was working on. Additionally, their effectiveness scores and categorization needed to be mapped onto ours to ensure consistency within our database to make it searchable. 

```sh
def map_to_categories(initial_categories):
    """Function takes the initial categories as a list and maps them onto broader categories. Returns a string.
    Returns the category if charity matches only one. Otherwise returns most specific category in the list. 
    """
    categories = set()
    for lable in initial_categories:
        if lable in topics_dict:
            categories.add(topics_dict[lable])
        else:
            categories.add("other")
    elif "nutrition and industrial livestock alternatives" in categories:
        return "nutrition and industrial livestock alternatives"

```
**STATISTICAL ANALYSIS**
How does our algorithm determine what charity to recommend?

All features were categorized using their corresponding dictionary that assigns each feature an interpretable category level. For instance, in topic feature we have main topics and sub topics which are part of the their related main topic. here, we assign each main topic a numeric level and assign the sub topics of the main topic a numeric level that inreases for each sun topic by step of 1. then, we reached the last sub topic of the main topic, a numerical level + 5 were assigned to the next main topic and this process went on until reaching the last sub category or main category.
```sh
categ_category = []
for i in d['category']:
  categ_category.append([category_levels[x] for x in i])
```
When you (the user) set your preferences in our questionaire our algorithm assigns a value to each of your inputs, as shown for the 'continent' category. 
```sh
temp = []
for i in user_continent:
    temp.append(int(continent_levels.loc[continent_levels['continent'] == i,:]['levels']))
user_continent = temp
temp = []
```

Then, these scores get matched to charities, that exactly match your preferences. Each item contributes to the "similarity score", i.e. how similar the charity is to your preference. In a second step, the algorithem determines, which charities are the next closest matches, using the assigned values as a basis for vector distance calculations. It then ranks the charities it found based on the similarity score and shows you the once most closely matchin all your criteria. 


We also create visualizations about our database and about the results of the user preferences and display them on the website. 



## GitHub pages
[![pages-build-deployment](https://github.com/stonehenge0/Open_Sourcerers/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/stonehenge0/Open_Sourcerers/actions/workflows/pages/pages-build-deployment)

The website is generated from the content in the `docs/` folder and reachable under the url: [https://stonehenge0.github.io/Open_Sourcerers/](https://stonehenge0.github.io/Open_Sourcerers/). 

Once changes to the `docs/` folder are made, the website builds again automatically. 

You can see the current build status, as well as previous builds in the `Actions` tab of the repository, or by clicking on the symbol next to where the last commit shown (shows as a little ✖️ or ✔️). Clicking the symbol and then `Details` will lead you to an overview of the current build where you can also run the build again without needing to modify the files in `docs/` by clicking on `Re-run all jobs` in the top right. 

You can change the setup so that the website is generated from the root of the repository instead in `settings` > `pages`. An `index.html` file needs to be present in the root directory for the site to be displayed correctly. 

## Website with Python functionality
We are running our website on localhost.
I you want to host our website and have the Questionnaire-functions online, you need to create a WSGI-server. Please refer to the Flask Documentation "Deploying to production" for further information: https://flask.palletsprojects.com/en/2.3.x/deploying/
Please note that due to the size of the modules in our requirements.txt a free pythonanywhere-server is too small.

## Installation
See `requirements.txt` for a full list of requirements.
The fastest way to install the requirements is using [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/#use-pip-for-installing) and a [virtual environment](https://docs.python.org/3/tutorial/venv.html) (like [venv](https://docs.python.org/3/library/venv.html)).
> Make sure to substitute <name_of_vev> with an actual name for your environment.

```sh
python3 -m venv <name_of_venv>
source <name_of_venv>/bin/activate
pip install -r requirements.txt
```
If you want to host our website and have the Questionnaire-functions online, you need to create a WSGI-server. Please refer to the Flask Documentation "Deploying to production" for further information: https://flask.palletsprojects.com/en/2.3.x/deploying/
Please note that due to the size of the modules in our requirements.txt a free pythonanywhere-server is too small.

If your server is set up, execute "app.py" and open your url. You should now have full functionality.


## How to use and extend the project? (maybe)
The different .py skripts in the 'data' folder all work together to collect and clean the data from the four different charity evaluators we used. It also includs excel spreadsheets of our final version of the collected data (final_XX.xlsx), that can easily be downloaded to use the statistical skripts on the data. To recreate the sheets the user would have to run the different skripts for each Website in order (e.g. XX_get_data.py, XX_get_more_data.py, cleanup_XX.py). One way to extend the project would be to gather more data on charities, for example from other charity evaluators. The data used for the statistical analysis is formatted to an excel table with headings "name", "category", "x-crisis", "country", "continent", "efficiency", "evaluator" and "website" and modify the statistical analysis code to include the new data. 

The website runs via "app.py". As Flask handles the communication between backend and frontend an WSGI-server is required, if you want to access the website via the internet. See above for more details on installation.

If you want to add further html-pages, remember to create a new route in app.py and reference the new page on existing html-pages (via single button reference like our submit-questionnaire button or via the menu on all pages). You could also use our website with a different dataset. The safest way to do this is to write a python functoin that returns the data you would like to have displayed as a dict. the dict-structure we use is this:

result = {
    result1 : {
    "name":value,
    "category_g":value,
    "category_s":value,
    "xcrisis":"yes" OR "no",
    "country":value,
    "continent":value,
    "efficiency":value,
    "evaluator":value,
    "link_website":value,
    "link_cost":value
    },
    result2 : {
    "name":value,
    "category_g":value,
    "category_s":value,
    "xcrisis":"yes" OR "no",
    "country":value,
    "continent":value,
    "efficiency":value,
    "evaluator":value,
    "link_website":value,
    "link_cost":value
    },
    result3 : {
    "name":value,
    "category_g":value,
    "category_s":value,
    "xcrisis":"yes" OR "no",
    "country":value,
    "continent":value,
    "efficiency":value,
    "evaluator":value,
    "link_website":value,
    "link_cost":value
    }
}

Then update the @app.route('/submit_questionnaire') part in app.py to call your own function instead of doing_search.main(). If you use different keys in your dictionary or a different amount of results being displayed, remember to edit the result_to_html-function in the app.py-file.

--- explain in more detail?

## Group Details

Group Name: ApplyPY <br>
Group Leader: Emma Stein <br>
Group Members: Emma Stein, Lena-Sinwo Ngassa, Paula Kottwitz, Sina Garazhian <br>
Tutor: Lars Kaesberg <br>
<br>
We developed the idea of the project and set up the timeline together. For detailed information on who worked on which parts of the project refer to `contributions.md`.

## Data Sources
Charity evaluation data was collected from
* [GiveWell](https://www.givewell.org/)
* [Giving What We Can](https://www.givingwhatwecan.org/)
* [Deutsches Institut für soziale Fragen](https://www.dzi.de/)
* [Animal Charity Evaluators](https://animalcharityevaluators.org/)

## License
Include the project's license. Usually, we suggest MIT or Apache. Ask your supervisor. For example:

Licensed under the Apache License, Version 2.0 (the "License"); you may not use news-please except in compliance with the License. A copy of the License is included in the project, see the file [LICENSE](LICENSE).

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License

## License of this readme-template (remove this once you replaced this readme-template with your own content)
This file itself is partially based on [this file](https://gist.github.com/sujinleeme/ec1f50bb0b6081a0adcf9dd84f4e6271). 
