from scheduler import update_news
from scheduler import time_difference
from scheduler import update_covid
from scheduler import repeat_update

def test_update_covid():
    update_covid()

def test_update_news():
    update_news()

def test_time_difference():
    data = time_difference(14, 00, 00, 15, 00)
    assert data == 3600
