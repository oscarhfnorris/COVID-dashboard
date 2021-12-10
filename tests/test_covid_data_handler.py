from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_API_request
from covid_data_handler import schedule_covid_updates

from covid_data_handler import get_num_cases
from covid_data_handler import get_hospital_cases
from covid_data_handler import get_cum_deaths
from covid_data_handler import get_location
from covid_data_handler import covid_data_collector
from covid_data_handler import update_covid

import global_vars

test_dict = covid_API_request('England', 'nation')

def test_parse_csv_data():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639

def test_process_covid_csv_data():
    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data ( parse_csv_data (
            'nation_2021-10-28.csv' ) )
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544

def test_covid_API_request():
    data = covid_API_request()
    assert isinstance(data, dict)

def test_get_num_cases():
    global test_dict
    data = get_num_cases(test_dict)

def test_get_hospital_cases():
    global test_dict
    data = get_hospital_cases(test_dict)

def test_get_cum_deaths():
    global test_dict
    data = get_cum_deaths(test_dict)

def test_get_location():
    global test_dict
    data = get_location(test_dict)
    assert data == 'England'

def test_covid_data_collector():
    data = covid_data_collector()

def test_schedule_covid_updates():
    schedule_covid_updates(update_interval=10, update_name='update test')

def test_update_covid():
    global_vars.init()
    update_covid()