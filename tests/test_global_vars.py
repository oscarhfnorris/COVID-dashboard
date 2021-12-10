from global_vars import init
from global_vars import set_global_vars
from global_vars import set_articles
from global_vars import set_covid_data_list
from global_vars import set_updates
from global_vars import retrieve_articles
from global_vars import retrieve_covid_data_list
from global_vars import retrieve_updates
from global_vars import update_articles
from global_vars import update_covid_data_list
from global_vars import update_updates

def test_init():
    init()
    assert retrieve_articles() == []
    assert retrieve_covid_data_list() == []
    assert retrieve_updates() == []

def test_set_global_vars():
    set_global_vars()
    assert retrieve_articles() == []
    assert retrieve_covid_data_list() == []
    assert retrieve_updates() == []

def test_set_articles():
    data = set_articles()
    assert retrieve_articles() == []

def test_set_covid_data_list():
    data = set_covid_data_list()
    assert retrieve_covid_data_list() == []

def test_set_updates():
    data = set_updates()
    assert retrieve_updates() == []

def test_retrieve_articles():
    init()
    assert retrieve_articles() == []

def test_retrieve_articles():
    init()
    assert retrieve_covid_data_list() == []

def test_retrieve_articles():
    init()
    assert retrieve_updates() == []

def test_update_articles():
    init()
    update_articles([1, 2, 3])
    assert retrieve_articles() == [1 ,2, 3]

def test_update_covid_data_list():
    init()
    update_covid_data_list([1, 2, 3])
    assert retrieve_covid_data_list() == [1 ,2, 3]

def test_update_updates():
    init()
    update_updates([1, 2, 3])
    assert retrieve_updates() == [1 ,2, 3]
    