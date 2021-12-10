# Personalized Covid Dashboard
---
## Introduction
As part of the 2021 ECM1400 Computer Science course at University of Exeter, I have been tasked with creating a personalized covid dashboard which displays data retrieved from the the newsapi from https://newsapi.org and the
 NHS [uk-covid19 api](https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/pages/examples/general_use.html#import) 

## Prerequisites
Python 3.9.9

---
## Installation (MAC)
### 1. Making a Virtual Environment:
1. Open a command prompt and change the current directory (cd) to the root folder of the Personalised-COVID-dashboard.
2. Create the environment by entering the commands:
	`python3 -m venv .venv`
	`source .venv/bin/activate`

### 2. Installing the requirments:
 Next the requirements need to be installed from requirements.txt into the virtual environment. This can be done with the command:
	`pip3 install -r requirements.txt`
	
If this were to fail you can install all the requirements seperatly:
	`pip3 install uk-covid19`
	`pip3 install flask`
	`pip3 install pytest`
	`pip3 install pyLint`
	
---
## Using the application
### Accessing the covid dashboard:
1. Open a command prompt, making sure your current directory is in the root folder of Personalised-COVID-dashboard, *like in step one of Making a Virtual Environment* , then run the command below to start the server:
		`python3 flask_application.py`
2. Next open the url http://127.0.0.1:5000/ to access the HTML interface
	and you should be on a webpage which looks something like this:
	![[dashboard-preview.png]]
### How to interact with the interface
On the interface you see in the picture avove you can see:
- an empty *Scheduled updates:* panel on the left of the screen
- COVID-19 statistics in the middle under *COVID-19 Tracker*  as well as a *Schedule data updates* panel beneath it
- a news panel under *News headlines:* containing a list of news articles related to the filter terms in *config.json* (more about this later).
#### News headlines
You can dismiss articles by pressing the 'x' in the top right corner of the article widget; this will cause the article to not re-appear during program run time.
You can also access the webpage the article was retrievded from by pressing the blue "Read More" link at the bottom if each article widget.
#### Scheduling news and covid updates
You can enter the time you want an update to run, the update name, whether you want it to repeat every 24 hours, and whether you'd like to update covid and news data, just news or just covid. 

Then press the 'submit' button to make the update start.

To cancel an update you can press the 'x' on the top left of the update which removes it.
### Configuring the application
To configure the application you use the *config.json* file which is located in the root folder of the application. In the file you find a dictionary with keys which are used for the configeration of the application:
- **locatoin**: specifies the location where the local covid data is collected form
- **location_type**: used alongside location when quering the api. All information for differenet filters on location are available from the link at the top of this file under *uk-covid19* link.
- **national_location**: the country you are getting the covid data from (England, Scotland, Wales).
- **news_api_key** the key for the news api. This can be sourced from the newsapi website.
- **news_search_terms**: the terms used to query the news api for news articles.


---
## Testing
All tests are in the (root folder)/test folder, there are 4 modules being tested:
1. test_covid_data_handler.py which tests the covid_data_handler.py module
2. test_global_vars.py which tests the globa_vars.py module
3. test_news_data_handling.py which tests the news_data_handling.py module
4. test_scheduler.py which tests the scheduler.py module

### 1. Setting up the tests
You must mke sure you are in the virtual environment within the root folder of the project. You can tell you're in it if the line in your terminal starts with `(.venv)`

**The virtual environment will then need to be 'restarted'**

To do this, we deactivate the environment with the command:
`deactivate`
Then we now need to reactivate the environment:
`source .venv/bin/activate`
Then run the setup.py file by inputting the following into the terminal (don't forget the period):
`pip3 install -e .`

### 2. Running the Tests
To run the tests, simply run the command:
`pytest`

----
## Details

**Author:** Oscar Norris

**License:** MIT Locense

**Github:**  [oscarhfnorris/COVID-dashboard (github.com)](https://github.com/oscarhfnorris/COVID-dashboard)

**Acknowledgements:** 
- For the *KThread* Function on line 486 within scheduler.py :  https://web.archive.org/web/20130503082442/http:/mail.python.org/pipermail/python-list/2004-May/281943.html
- Hugo aBarbosa, Matt Collison








