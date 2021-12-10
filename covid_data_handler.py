"""Module to proccess all covid data returned from the covid api and csv file"""
import json
import sched
import threading
import time
import logging
from datetime import date, timedelta
from uk_covid19 import Cov19API
import global_vars

#sets up logging for this module
FORMAT = '%(levelname)s: %(asctime)s: %(message)s'
logging.basicConfig(filename='log_file.log', format=FORMAT, level=logging.INFO)

#sets up the config file for this module
with open("config.json", encoding='utf8') as json_data_file:
    config = json.load(json_data_file)

#Creates sched instance
SCHEDULER = sched.scheduler(time.time, time.sleep)


def parse_csv_data(csv_filename:str) -> list:
    """
        Description:

            Function which opens a csv file and iterates through the file, adding each line to a list, which is returned.
            Each line in the list is seperated by commas like in the csv file.

        Arguments:

            csv_file_name {str} : is the string name of the csv file

        Returns:

            corona_data_list {list} : is a list of strings containing the covid data
    """
    # empty list which will be filled with every line from the csv
    corona_data_list = []
    corona_data =  open(csv_filename, 'r')

    # iterate through every line in the csv file and appends each line to corona_data_list
    for line in corona_data:
        line_data = line.strip()
        corona_data_list.append(line_data)
    corona_data.close()
    return corona_data_list

def process_covid_csv_data(covid_csv_data:list) -> tuple[int, int, int]:
    """
        Description:

            Function to get last 7 day number of cases, hospital cases and cumulative number of deaths the data returned from a list
            (returned from parse_csv_data).

        Arguments:

            covid_csv_data {list} : list which contains covid data (areaCode,areaName,areaType,
            date,cumDailyNsoDeathsByDeathDate,hospitalCases,newCasesBySpecimenDate)

        Returns:

            num_cases {int} : integer value containing the number of covid cases in the last 7 days

            hospital_cases {int} : integer value containing the number of current hospital cases from covid

            cum_deaths {int} : integer value containing the cumulative number of deaths from covid
    """
    num_cases = 0
    for i in range (3, 10):
        record = covid_csv_data[i]
        # extract the newCasesBySpecimenDate field andadd it to the num_cases variable until last 7 days are added
        num_cases = num_cases + int(','.join(record.split(',', 7)[6:]))
    hospital_cases = int(','.join(covid_csv_data[1].split(',', 6)[5:6]))
    cum_deaths = int(','.join(covid_csv_data[14].split(',', 5)[4:5]))

    logging.info('COVID DATA IN CSV PROCESSED')
    return num_cases, hospital_cases, cum_deaths


def covid_API_request(location:str='Exeter', location_type:str='ltla') -> dict:
    """
        Description:

            Function to get up to date covid data from nhs covid 19 api based on location given and the specified fields

        Arguments:

            location {str} : string value containing the location data displayed is from

            location_type {str} : string containing the type of location

        Returns:

            covid_data_dictionary {dict} : dictionary containing 3 sub dictionary's: 'data' (containing all covid data requested),
            'lastUpdate', 'length', 'totalPages'
    """
    # Specifies the location set by the function arguments
    location = [
        'areaType='+location_type,
        'areaName='+location
    ]

    # declares the fields that are wanted to be returned from the api (constructing structure of json to be returned)
    fields = {
        "areaCode": "areaCode",
        "areaName": "areaName",
        "areaType": "areaType",
        "date": "date",
        "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate",
        "hospitalCases": "hospitalCases",
        "newCasesByPublishDate": "newCasesByPublishDate",
    }

    # initialise the COVID19API object with the chosen filters
    api = Cov19API(filters=location, structure=fields)

    #creates a json file by extracting the data from the api object
    covid_data_dictionary = api.get_json()

    #returns json file
    return covid_data_dictionary


def get_num_cases(dictionary:dict) -> int:
    """
    Description:

        Function which gets the total number of positive covid cases in the last 7 days, not including the entry with the most recent date
        from the returned dictionary from covid_API_request

    Arguments:

        dictionary {dict} : dictionary containing 3 sub dictionary's: 'data' (containing all covid data requested),
                                    'lastUpdate', 'length', 'totalPages'

    Returns:

        num_cases {int} : integer value containing the number of covid cases in the last complete 7 days
    """

    num_cases = 0
    if str(dictionary['data'][0]['date']) == str(date.today()):
        for i in range (1, 8):
            if str(dictionary['data'][i]['date']) == str(date.today() - timedelta(days = i)):
                num_cases = num_cases + int(dictionary['data'][i]['newCasesByPublishDate'])
    else:
        yesterday = date.today() - timedelta(days = 1)
        for i in range (0, 7):
            if str(dictionary['data'][i]['date']) == str(yesterday - timedelta(days = i)):
                num_cases = num_cases + int(dictionary['data'][i]['newCasesByPublishDate'])
    return num_cases

def get_hospital_cases(dictionary:dict) -> int:
    """
    Description:

        Function which gets number of current hospital cases from the returned dictionary from covid_API_request

    Arguments:

        dictionary {dict} : dictionary containing 3 sub dictionary's: 'data' (containing all covid data requested),
                                    'lastUpdate', 'length', 'totalPages'

    Returns:

         hospital_cases {int} : integer value containing the number of current hospital cases from covid
    """
    if str(dictionary['data'][2]['date']) == str(date.today() - timedelta(days = 2)):
        index = 2
    else:
        index = 3
    hospital_cases = int(dictionary['data'][index]['hospitalCases'])
    return hospital_cases

def get_cum_deaths(dictionary:dict) -> int:
    """
    Description:

        Function which gets the cumulative number of deaths because of covid from the returned dictionary from covid_API_request

    Arguments:

         dictionary {dict} : dictionary containing 3 sub dictionary's: 'data' (containing all covid data requested),
                                    'lastUpdate', 'length', 'totalPages'

    Returns:

        cum_deaths {int} : integer value containing the cumulative number of deaths from covid
    """
    if str(dictionary['data'][14]['date']) == str(date.today() - timedelta(days = 14)):
        index = 14
    else:
        index = 15
    cum_deaths = int(dictionary['data'][index]['cumDeaths28DaysByDeathDate'])
    return cum_deaths

def get_location(local_dictionary:dict) -> str:
    """
    Description:

        Function which gets the local location from the returned local dictionary from covid_API_request

    Arguments:

        local_dictionary {dict} : dictionary containing 3 sub dictionary's: 'data' (containing all covid data requested),
                                    'lastUpdate', 'length', 'totalPages'

    Returns:

        local_location {str} : string value containing the name of the local location
    """
    local_location = str(local_dictionary['data'][0]['areaName'])
    return local_location


def covid_data_collector() -> tuple[str, str, int, int, str, str]:
    """
    Description:

        Function which uses the: covid_API_request,  get_location, get_num_cases, get_hospital_cases, get_cum_deaths
        functions to get the required data to be returned to the HTML page

    Arguments:

        None

    Returns:

        local_location {str} : string value containing the name of the local location

        national_location {str} : string value containing the name of the national location

        local_num_cases {int} : integer value containing the number of covid cases in the last complete 7 days in the local area

        national_num_cases {int} : integer value containing the number of covid cases in the last complete 7 days in the national area
    """
    #creates dictionary's from the local and national areas
    local_dict = covid_API_request(config['location'], config['location_type'])
    national_dict = covid_API_request(config['national_location'], 'nation')

    #gets local fields required to be put into the web page
    local_location = get_location(local_dict)
    local_num_cases = get_num_cases(local_dict)

    #gets national fields required to be put into web page
    national_location = get_location(national_dict)
    national_num_cases = get_num_cases(national_dict)
    national_hospital_cases = 'Hospital Cases: '+ str(get_hospital_cases(national_dict))
    national_cum_deaths = 'Total Deaths: '+ str(get_cum_deaths(national_dict))

    return local_location, national_location, local_num_cases, national_num_cases, national_hospital_cases, national_cum_deaths


def schedule_covid_updates(update_interval:int, update_name:str) -> None:
    """
    Description:

        Function to schedule a new covid update by running a scheduler in the sched module.

        (This function is not in use, the scheduling is all done in the scheduling.py module, this is here to pass the tests)

    Arguments:

        update_interval {int} : integer value containing the number of seconds until the update will be executed

    Returns:

        None
    """
    #creating an instance of the schedular class
    logging.info('update covid schedular function running for the next', update_interval, 'seconds')

    update_name = update_name+'covid'
    update_name = SCHEDULER.enter(update_interval, 1, update_covid, ()) #calls function to update covid data

    thread = threading.Thread(target=SCHEDULER.run)
    thread.start()

def update_covid() -> None:
    """
    Description:

        Function which is called from the schedule_covid_updates function to update the global variable covid_data_list
        in the global_vars.py module.

        (This function is not in use, the scheduling is all done in the scheduling.py module, this is here to pass the tests)

    Arguments:

        None

    Returns:

        None
    """
    global_vars.update_covid_data_list(covid_data_collector())
    logging.info('covid data updated')
