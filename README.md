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
The ApplePy Charity pickers helps you find a charity to donate to. Over our website, the user can enter their preferences and we will suggest charities from our database that most closely match what they are looking for and give out additional information on the charity's cost-effectiveness and more. 

## Motivation
The motivation behind this project was to combine multiple charity sources and extend their original functionalities to have a database of searchable, topically diverse, and cost-effective charities.

- *Searchable*: Charity evaluators often recommended charities, but did not make their data available in a structured and searchable manner. We extracted their data and processed it in a way that would allow users to navigate these charities easier and find what they were looking for. 
- *Topically diverse*: Our sources consist of charity evaluators focusing on animal charities, charities with high cost-efficiency, longterm impact charities and a more broad evaluator. By bringing those different approaches together and fitting them into one database, we offer a wide range of charities to explore.
- *High quality charities and detailed cost-efficiency information*: By sourcing only from known charity evaluators we ensure that the charities we recommend are high-quality. We also sourced detailed cost-effectiveness analysis of each charity for the user to inspect themselves. 

Another major point of consideration was to make picking a high-quality charity as easy as possible. One major obstacle to effective giving is the effort required to look through different evaluators and find the right charity to donate to. Our website provides easy access to these functionalities and does not require users to have coding knowledge in order to make it more accessible. 

## Features
- A database consisting of four different evaluators each focusing on different aspects of charitable giving. Their data has been extended to include links to the charities, geographic information, in-depth cost-effectiveness analyses and more. 
- An algorithm to match user preferences with the charities in our database and return close matches.
- Visualizations about our data sources and the results our algorithm produces.
- An easy to use website, so users without coding experience can acces our functionalities.


## Code examples
We first read in the data that we have from each of our sources, in this case using webscraping with [Beautiful soup](https://pypi.org/project/beautifulsoup4/).

> Note: the process of extracting, processing and scraping data varies strongly between our sources. In favour of simplicity, the data collection process will be shown at the example of ACE (Animal Charity Evaluator) here.

```sh
    # We used BeautifulSoup to webscrape data from the individual ACE charity websites. 
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

All features were categorized using their corresponding dictionary that assigns each feature an interpretable category level. For instance, in the topic feature, we have main topics and sub-topics which are part of their related main topic. here, we assign each main topic a numeric level and assign the sub-topics of the main topic a numeric level that increases for each sun topic by 1 level. Then, we reached the last sub-topic of the main topic, a numerical level + 5 was assigned to the next main topic and this process went on until reaching the last sub-category or main category.
```sh
categ_category = []
for i in d['category']:
  categ_category.append([category_levels[x] for x in i])
```

Topic | levels |
 ---- | --- |
infrastructure | 1 | 
rural areas	 | 6 |
healthcare and prevention | 11 |
maternal and neonatal health | 12 |	
vaccinations | 13 |
Malaria | 14 |
HIV/AIDS | 15 |	
orthopedic treatment | 16 |
children, youth and family | 21 |



When you (the user) set your preferences in our questionnaire and select how different features are important for him/her, our algorithm assigns a value to each of your inputs, as shown for the 'continent' category. 
```sh
temp = []
for i in user_continent:
    temp.append(int(continent_levels.loc[continent_levels['continent'] == i,:]['levels']))
user_continent = temp
temp = []
```

Then, these scores get matched to charities, that exactly match your preferences. Each item contributes to the "similarity score", i.e. how similar the charity is to your preference. In a second step, the algorithem determines, which charities are the next closest matches, using the assigned values as a basis for vector distance calculations. It then ranks the charities it found based on the similarity score and shows you the one that most closely matches all your criteria.
in the below code example, the algorithm tries to give any match 5 scores. moreover, the algorithm gives between 1 to 3 scores to close matches for the topic category. here, the column and wanted arguments are the feature and user input, respectively. moreover, the feature argument is only set to True for topics and efficiency features because their categorization method is more meaningful than other feature categorization methods.
```sh
  def iterate_1(amount, vec):
    dists = [((amount-x)**2)**0.5 for x in vec if ((amount-x)**2)**0.5 <= 3]
    try:
      return(min(dists))
    except Exception:
      return(0)
  def calculate_over_all(column, wanted, feature = False):
    scores = []
    k = 0
    try:
      desired_vector = ast.literal_eval(column)
    except Exception:
      desired_vector = column

    for i in wanted:
      if i in desired_vector:
        k = k + 10
      elif i not in desired_vector and feature:
        k = k + iterate_1(i,desired_vector)
    return(k)
  total_scores = []
  for index, row in f.iterrows():
    v_1 = calculate_over_all(row['categ_continent'], user_continent)

  #print(row['efficiency'])
    v_2 = calculate_over_all([row['efficiency']], user_eff, True)
  #print(row['country'])
    v_3 = calculate_over_all(row['categ_country'], user_country)
    v_4 = calculate_over_all(row['categ_category'], user_category, True)
  #print(row['categ_x'])
    v_5 = calculate_over_all([row['categ_x']], user_x, 1)
    total_scores.append((v_1+v_2+v_3+v_4+v_5))
  ##sort the results based on their similarity score
  emp_dic = {}
  k = 0
  for i in total_scores:
    emp_dic[k] = i
    k = k + 1
  sorted_dic = dict(sorted(emp_dic.items(), key=lambda x:x[1] , reverse= True))

```


We also create visualizations about our database and about the results of the user preferences and display them on the website. 
The code example below tries to depict a pie chart of similarity scores for top-found charities.
```sh
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.pie(counts, labels=names, autopct='%1.1f%%')
```



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
```sh
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
```

Then update the @app.route('/submit_questionnaire') part in app.py to call your own function instead of doing_search.main(). If you use different keys in your dictionary or a different amount of results being displayed, remember to edit the result_to_html-function in the app.py-file.


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
This project is covered through a MIT License.

Copyright (c) 2024 Emma Victoria Stein

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

> See [LICENSE](LICENSE.txt).

