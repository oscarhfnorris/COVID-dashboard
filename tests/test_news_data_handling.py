from covid_news_handling import news_API_request
from covid_news_handling import update_news
from covid_news_handling import find_article
from covid_news_handling import news_dictionary_maker
from covid_news_handling import article_seen
import global_vars

# setup data for test
global_vars.init()


def test_news_API_request():
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()

def test_update_news():
    update_news('test')

def test_find_article():
    global_vars.update_articles([{
        'seen' : 0,
        'articles' : {'title' : 'this is a title', 'url' : 'this is a url'}
    }])
    assert find_article('this is a url') == True

def test_news_dictionary_maker():
    data = news_dictionary_maker(update_news())
    assert len(data) > 0

def test_article_seen():
    global_vars.update_articles([{
        'seen' : 0,
        'articles' : {'title' : 'this is a title', 'url' : 'this is a url'}
    }])
    article_seen('this is a title')
    assert global_vars.retrieve_articles()[0]['seen'] == 1
