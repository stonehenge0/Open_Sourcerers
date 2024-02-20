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


After extracting the data, we see what the data is missing to fit in our schema: In this case ACE did not specify the continents that a charity was working on. Additionally, their effectiveness scores and categorization needed to be mapped onto ours to ensure consistency within our database to make it searchable. 

```sh
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
    elif "nutrition and industrial livestock alternatives" in categories:
        return "nutrition and industrial livestock alternatives"

```
**insert STATISTICAL ANALYSIS (Sina) here**

We also create visualizations about our database and about the results of the user preferences and display them on the website. 



## GitHub pages/ Website
[![pages-build-deployment](https://github.com/stonehenge0/Open_Sourcerers/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/stonehenge0/Open_Sourcerers/actions/workflows/pages/pages-build-deployment)

The website is generated from the content in the `docs/` folder and reachable under the url: [https://stonehenge0.github.io/Open_Sourcerers/](https://stonehenge0.github.io/Open_Sourcerers/). 

Once changes to the `docs/` folder are made, the website builds again automatically. 

You can see the current build status, as well as previous builds in the `Actions` tab of the repository, or by clicking on the symbol next to where the last commit shown (shows as a little ✖️ or ✔️). Clicking the symbol and then `Details` will lead you to an overview of the current build where you can also run the build again without needing to modify the files in `docs/` by clicking on `Re-run all jobs` in the top right. 

You can change the setup so that the website is generated from the root of the repository instead in `settings` > `pages`. An `index.html` file needs to be present in the root directory for the site to be displayed correctly. 


## Installation
See `requirements.txt` for a full list of requirements.
The fastest way to install the requirements is using [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/#use-pip-for-installing) and a [virtual environment](https://docs.python.org/3/tutorial/venv.html) (like [venv](https://docs.python.org/3/library/venv.html)).
> Make sure to substitute <name_of_vev> with an actual name for your environment.

```sh
python3 -m venv <name_of_venv>
source <name_of_venv>/bin/activate
pip install -r requirements.txt
```




## How to use and extend the project? (maybe)
Include a step-by-step guide that enables others to use and extend your code for their projects. Whether this section is required and whether it should be part of the `README.md` or a separate file depends on your project. If the **very short** `Code Examples` from above comprehensively cover (despite being concise!) all the major functionality of your project already, this section can be omitted. **If you think that users/developers will need more information than the brief code examples above to fully understand your code, this section is mandatory.** If your project requires significant information on code reuse, place the information into a new `.md` file.

## Results
If you performed evaluations as part of your project, include your preliminary results that you also show in your final project presentation, e.g., precision, recall, F1 measure and/or figures highlighting what your project does. If applicable, briefly describe the dataset your created or used first before presenting the evaluated use cases and the results.

If you are about to complete your thesis, include the most important findings (precision/recall/F1 measure) and refer to the corresponding pages in your thesis document.

## License
Include the project's license. Usually, we suggest MIT or Apache. Ask your supervisor. For example:

Licensed under the Apache License, Version 2.0 (the "License"); you may not use news-please except in compliance with the License. A copy of the License is included in the project, see the file [LICENSE](LICENSE).

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License

## License of this readme-template (remove this once you replaced this readme-template with your own content)
This file itself is partially based on [this file](https://gist.github.com/sujinleeme/ec1f50bb0b6081a0adcf9dd84f4e6271). 
