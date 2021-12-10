"""Module to proccess all news data returned from the news api"""
import json
import logging
import requests
from flask import Markup
import global_vars

#sets up logging for this module
FORMAT = '%(levelname)s: %(asctime)s: %(message)s'
logging.basicConfig(filename='log_file.log', format=FORMAT, level=logging.INFO)

#sets up the config file for this module
with open("config.json", encoding='utf8') as json_data_file:
    config = json.load(json_data_file)


def news_API_request(covid_terms:str='Covid COVID-19 coronavirus') -> dict:
    """
    Description:

        Function to return dictionary of covid news articles retrieved from the news api

    Arguments:

        covid_terms {str} : string containing the terms used as a filter when returning the news articles form the api

    Returns:

        news_dict {dict} : dictionary containing the news articles under the 'articles' key
    """
    # specifies the filters for returning the news
    url = ('https://newsapi.org/v2/everything?'
        'q=' + covid_terms + '&'
        'from=2021-11-18&'
        'sortBy=popularity&'
        'apiKey='+config['news_api_key'])

    # retrieves the dictionary from the API
    news_dict = requests.get(url).json()
    return news_dict


def update_news(articles:list=[], news_filter_terms:str='Covid COVID-19 coronavirus') -> list:
    """
    Description:

        Function to create or update a data structure which contains news articles found and used during program run-time.

        The data structure is a list of dictionary's each containing keys::
            (1) 'seen' {int} : which is 0 until a news article has been removed from the HTML with the 'x'
            (2) 'articles' {dict} : which contains the articles returned from the news_API_request function

    Arguments:

        articles {list} : list contaiing a list of dictionary's' (as described above)

        news_filter_terms {str} : string containing the terms used as a filter when returning the news articles form the api

    Returns:

        articles {list} : list contaiing a list of dictionary's' (as described above). It has been updated.
    """
    if articles == 'test':
        articles = []
    # gets newest articles list from news api dictionary which is returned
    news_list = news_API_request(news_filter_terms)['articles']
    # adds link to the url website
    news_list = add_link(news_list)
    # appends newsest articles from new api to the articles list before anything else
    x = 0
    for i in news_list:
        article_dict = news_list[x]

        # won't append any news articles which are already on the list
        if find_article(article_dict['url']):
            continue

        # adds dictionary to each list index
        articles.append({
                                    'seen' : 0,
                                    'articles': article_dict
                                })
        x = x + 1
    return articles


def find_article(url:str) -> bool:
    """
    Description:

        Function to see if an article is already present in the articles list. Used to get rid of repeat articles before being added to the global articles list

    Arguments:

        url {str} : string containing the url of an article, it is treated like a primary key in a database (unique identifier)

    Returns:

        {bool} : True if the article is already present in the list
    """
    articles = global_vars.retrieve_articles()
    if len(articles) == 0:
        # returns False if the list is empty (meaning that the update_news function is running for the first time)
        return False

    x = 0
    for i in articles:
        if url == articles[x]['articles']['url']:
            return True
        x = x + 1
    return False


def news_dictionary_maker(articles_list:list) -> list:
    """
    Description:

        Function to make a smaller list which doesn't contain the 'seen' key

    Arguments:

        articles_list {list} : list contains dictionary's with the 'seen' and 'articles' keys

    Returns:

        news_list {list} : list containing just the 'articles' jey from the list in arguments
    """
    news_list = []
    # cycles through each news article and appends dictionary if article hasn't been seen before
    x = 0
    for i in articles_list:
        if articles_list[x]['seen'] == 0:
            news_list.append(articles_list[x]['articles'])
        x = x + 1

    return news_list


def article_seen(article_title:str) -> list:
    """
    Description:

        Function to turn a certain article to seen if the user has clicked the 'x' on a news article.

    Arguments:

        article_title {str} : string containing the title of an article the user has pressed 'x' on

    Returns:

        articles {list} : list contaiing a list of dictionary's. The article the user pressed 'x' on has key 'seen' set to 1
    """
    articles = global_vars.retrieve_articles()
    # cycles through each article in the data structure, if it finds teh correct article, it changes the 'seen' key for that article to 1
    x = 0
    for i in articles:
        if article_title == articles[x]['articles']['title']:
            articles[x]['seen'] = 1
        x = x + 1
    return articles


def add_link(news_list:list) -> list:
    """
    Description:

        Function to remove the readmore and the add the url as a marked up link for the 'content' key in the 'articles' dictionary.

    Arguments:

        news_list {list} : list containing the news articles dictionaries

    Returns:

        news_list {list} : list containing the news articles dictionaries
    """
    x = 0
    for i in news_list:
        # retrieves the content t be changed
        content = news_list[x]['content']
        # retrieves the url to be added to content
        url = news_list[x]['url']

        size = len(content)
        # removes [readmore] and adds the link to the webpage in markup
        content = content[:size-13].replace('[', '') + Markup(f"<a href='{url}'>Read More</a>")

        # adds the new content
        news_list[x]['content'] = content
        x = x + 1
    return news_list
