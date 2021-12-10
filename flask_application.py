"""Module to interact with the HTML user interface"""
import logging
from flask import Flask, request
from flask.templating import render_template
from covid_data_handler import covid_data_collector
from covid_news_handling import update_news
from covid_news_handling import news_dictionary_maker
from covid_news_handling import article_seen
import global_vars
from scheduler import get_interval
from scheduler import append_updates_list
from scheduler import name_in_use
from scheduler import remove_update
from scheduler import find_dictionary_key

# sets up logging for this module
FORMAT = '%(levelname)s: %(asctime)s: %(message)s'
logging.basicConfig(filename='log_file.log', format=FORMAT, level=logging.INFO)

# sets all of the global variables to empty lists
global_vars.set_global_vars()

# sets up the flask application
app = Flask(__name__)

@app.route('/')
def index() -> str:
    """
    Description:

        Function which gathers the required data to be rendered on the HTML interface with the render_template function.

    Arguments:

        None

    Returns in render_template function:

        'COVID-19 Tracker' {str} : string containing Title displayed on HTML

        covid_data_list[0] {str} : string containing the local location displayed on HTML

        covid_data_list[1] {str} : string containing national location displayed on HTML

        covid_data_list[2] {str} : string containing local 7 day infection rateisplayed on HTML

        covid_data_list[3] {str} : string containing national 7 day infection rate displayed on HTML

        covid_data_list[4] {str} : string containing national current hospital cases displayed on HTML

        covid_data_list[5] {str} : string containing the total cumulative deaths displayed on HTML

        news_articles[0:4] {list} : list containing the first 4 items in a list of the news articles

        '/static/images/shark.gif' {str} : string containing the file location of a picture used as the favicon

        'shark.gif' {str} : string containing the file location of a picture used as the icon
    """

    logging.info('LOADED: index()')

    # collects all data to do with covid data
    global_vars.update_covid_data_list(covid_data_collector())
    covid_data_list = global_vars.retrieve_covid_data_list()

    # puts all news articles in articles list
    global_vars.update_articles(update_news())
    # creates news list to be put on html
    news_articles = news_dictionary_maker(global_vars.retrieve_articles())

    return render_template('index.html',
                            title='COVID-19 Tracker',
                            location=covid_data_list[0],
                            nation_location=covid_data_list[1],
                            local_7day_infections=covid_data_list[2],
                            national_7day_infections=covid_data_list[3],
                            hospital_cases=covid_data_list[4],
                            deaths_total=covid_data_list[5],
                            news_articles=news_articles[0:4],
                            favicon='/static/images/shark.gif',
                            image='shark.gif'
                        )


@app.route('/index', methods = ['GET'])
def index2() -> str:
    """
    Description:

        Function which gathers the required data to be rendered on the HTML interface with the render_template function.

        And also gets the outputs from interface interactions (scheduling updates)

    Arguments:

        None

    Returns in render_template function:

        'COVID-19 Tracker' {str} : string containing Title displayed on HTML

        covid_data_list[0] {str} : string containing the local location displayed on HTML

        covid_data_list[1] {str} : string containing national location displayed on HTML

        covid_data_list[2] {str} : string containing local 7 day infection rateisplayed on HTML

        covid_data_list[3] {str} : string containing national 7 day infection rate displayed on HTML

        covid_data_list[4] {str} : string containing national current hospital cases displayed on HTML

        covid_data_list[5] {str} : string containing the total cumulative deaths displayed on HTML

        news_articles[0:4] {list} : list containing the first 4 items in a list of the news articles

        '/static/images/shark.gif' {str} : string containing the file location of a picture used as the favicon

        'shark.gif' {str} : string containing the file location of a picture used as the icon
    """

    logging.info('LOADED: index2() ')

    # Functions for deleting updates and news articles
    news_delete_request()
    update_delete_request()

    # collects all data to do with covid data
    covid_data_list = global_vars.retrieve_covid_data_list()

    # creates news list to be put on html
    news_articles = news_dictionary_maker(global_vars.retrieve_articles())

    # retrieves update list to put in html
    update_list = global_vars.retrieve_updates()

    # scheduling
    # name of the update
    if request.args.get('two'):
        update_name = request.args.get('two')

        # if user presses the repeat button then repeat is True
        if request.args.get('repeat'):
            repeat = True
        else:
            repeat = False

        # if user presses update covid data button
        if request.args.get('covid-data'):
            update_covid_data = True
        else:
            update_covid_data = False

        # if user presses the news update button
        if request.args.get('news'):
            update_news = True
        else:
            update_news = False

        # time of update
        if request.args.get('update'):
            update_time = request.args.get('update')
            # new update
            seconds_until_update = get_interval(update_time)
            skip = False
        else:
            skip = True

        # checks if update name is already in use
        if name_in_use(update_name):
            skip = True


        # Gets type of update
        if update_covid_data or update_news or skip:
            if update_covid_data and update_news and skip is False:
                update_type = 'cn' # meaing covid (c) and news (n)
            elif update_covid_data and skip is False:
                update_type = 'c' # meaning covid (c)
            elif update_news and skip is False:
                update_type = 'n' # meaning news (n)
            else:
                skip = True
        else:
            skip = True

        # Creates new update item on the updates list
        if skip is not True:
            # appends the update to the updates list
            append_updates_list(update_type, repeat, update_name, update_time, seconds_until_update)


    return render_template('index.html',
                            title='COVID-19 Tracker',
                            location=covid_data_list[0],
                            nation_location=covid_data_list[1],
                            local_7day_infections=covid_data_list[2],
                            national_7day_infections=covid_data_list[3],
                            hospital_cases=covid_data_list[4],
                            deaths_total=covid_data_list[5],
                            news_articles=news_articles[0:4],
                            updates=update_list,
                            favicon='/static/images/shark.gif',
                            image='shark.gif'
                        )


def news_delete_request() -> None:
    """
    Description:

        Function to mark articles as 'seen'. When the 'x' is pressed on the news article, the article is set as seen with the article_seen function.

        The articles variable is updated globally.

    Arguments:

        None

    Returns:

        None
    """
    if request.args.get('notif'):
        # getting input with notif = news article title in HTML form
        news_title = request.args.get('notif')

        # adds new news
        global_vars.update_articles(article_seen(news_title))

        log = 'REMOVED NEWS ARTICLE:', news_title
        logging.info(log)


def update_delete_request() -> None:
    """
    Description:

        Function to remove updates form the global updates list. When the 'x' is pressed on the updates, the update is removed from the global updates list.

    Arguments:

        None

    Returns:

        None
    """
    if request.args.get('update_item'):
        # gets name of the update to be removed
        update_name = request.args.get('update_item')
        update_time = find_dictionary_key(update_name, 'title', 'update_time', global_vars.retrieve_updates())

        global_vars.update_updates(remove_update(update_name, global_vars.retrieve_updates()))
 
        if global_vars.retrieve_updates() == None:
            global_vars.update_updates([])

        log = 'REMOVED UPDATE:', update_name, 'at', update_time
        logging.info(log)


# runs the flask application
if __name__ == '__main__':
    app.run()
