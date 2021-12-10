"""Module used to set, update and retrieve the global articles"""
ARTICLES = []
COVID_DATA_LIST = []
UPDATES = []

def init() -> None:
    """
    Definition:

        Initiates the global_vars module
    """
    set_global_vars()

def set_global_vars() -> None:
    """
    Defintion:

        Sets the global variables with their set functions
    """
    set_articles()
    set_covid_data_list()
    set_updates()


def set_articles() -> None:
    """
    Definition:

        Sets the 'ARTICLES' global variable
    """
    global ARTICLES
    ARTICLES = []

def set_covid_data_list() -> None:
    """
    Definition:

        Sets the 'COVID_DATA_LIST' global variable
    """
    global COVID_DATA_LIST
    COVID_DATA_LIST = []

def set_updates() -> None:
    """
    Definition:

        Sets the 'UPDATES' global variable
    """
    global UPDATES
    UPDATES = []


def retrieve_articles() -> None:
    """
    Definition:

        Retrieves the 'ARTICLES' global variable
    """
    global ARTICLES
    if 'ARTICLES' not in globals():
        ARTICLES = []
    return ARTICLES

def retrieve_covid_data_list() -> None:
    """
    Definition:

        Retrieves the 'COVID_DATA_LIST' global variable
    """
    global COVID_DATA_LIST
    return COVID_DATA_LIST

def retrieve_updates() -> None:
    """
    Definition:

        Retrieves the 'UPDATES' global variable
    """
    global UPDATES
    return UPDATES


def update_articles(input:list) -> None:
    """
    Definition:

        Updates the 'ARTICLES' global variable

    Arguments:

        input {list} : the list which will update
    """
    global ARTICLES
    ARTICLES = input

def update_covid_data_list(input:list) -> None:
    """
    Definition:

        Updates the 'COVID_DATA_LIST' global variable

    Arguments:

        input {list} : the list which will update
    """
    global COVID_DATA_LIST
    COVID_DATA_LIST = input

def update_updates(input:list) -> None:
    """
    Definition:

        Updates the 'UPDATES' global variable

    Arguments:

        input {list} : the list which will update
    """
    global UPDATES
    UPDATES = input
