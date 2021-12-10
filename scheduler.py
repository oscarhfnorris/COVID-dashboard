"""Module used for scheduling covid and news updates"""
import json
import  sched
import  time
import  threading
import  sys
import logging
from datetime import datetime
import  global_vars
from covid_data_handler import covid_data_collector
from covid_news_handling import update_news

# sets up logging for this module
FORMAT = '%(levelname)s: %(asctime)s: %(message)s'
logging.basicConfig(filename='log_file.log', format=FORMAT, level=logging.INFO)

#sets up the config file for this module
with open("config.json") as json_data_file:
    config = json.load(json_data_file)

# creates sched instance
SCHEDULER = sched.scheduler(time.time, time.sleep)

# global variable for this module is set
ACTIVE_SCHEDS = []


def schedule_covid_updates(update_interval:int, update_name:str, repeat:bool, update_type:str, update_time:str) -> sched.Event:
    """
    Description:

        Function to schedule updates from the covid API requests by creating instances of the sched class.
        There are three sched events created:

            repeat_sched : only created if the update is going to repeat every 24 hours. Calls the repeat_update function

            update_name : calls the update_covid function

            cancel_sched : calls the remove_updates function. Run when the data has been updated

        SCHEDULER instance is run in another thread with with the Kthread class.

        Sched event names are added to a list of dictionary's, ACTIVE_SCHEDS, so that the
        threads can be terminated of the user cancles an update

    Arguments:

        update_interval {int} : integer value showing the number of seconds until the update function is run from the sched object

        update_name {str} : string containing the name of the update

        repeat {bool} : boolean stating whether the update will repeat every 24 hours or not

        update_type {str} : string which states whether the update will update news, covid data or news and covid data

        update_time {str} : string containing the time update function will be run

    Returns:

        None
    """
    sched_name = update_name
    log = 'COVID UPDATE SCHED INSTANCE,', update_name, ', RUNNING FOR', update_interval, 'SECONDS UNTIL', update_time
    logging.info(log)

    if repeat:
        repeat_sched = SCHEDULER.enter(update_interval, 1, repeat_update, (update_type, update_name, update_time))
        logging.info('EVERY 24 HOURS')

    update_name = update_name+'covid'
    update_name = SCHEDULER.enter(update_interval, 2, update_covid, ())

    cancel_sched = sched_name+'covid_cancel'
    cancel_sched = SCHEDULER.enter(update_interval, 3, remove_update, (sched_name, global_vars.retrieve_updates(), False))

    covid_thread = KThread(target=SCHEDULER.run)
    covid_thread.start()

    ACTIVE_SCHEDS.append({
                        'sched_name' : sched_name, # acts as primary key
                        'sched' : update_name,
                        'cancel_sched' : cancel_sched,
                        'thread_name' : covid_thread
    })

    return ACTIVE_SCHEDS

def update_covid() -> None:
    """
    Description:

        Function which updates the global variable covid_data_list with new covid data by calling the covid_data_collector function

    Arguments:

        None

    Returns:

        None
    """
    global_vars.update_covid_data_list(covid_data_collector())
    logging.info('COVID UPDATED')


def schedule_news_updates(update_interval:int, update_name:str, repeat:bool, update_type:str, update_time:str) -> sched.Event:
    """
    Description:

        Function to schedule updates from the covid API requests by creating instances of the sched class.
        There are three sched events created:

            repeat_sched : only created if the update is going to repeat every 24 hours. Calls the repeat_update function

            update_name : calls the update_covid function

            cancel_sched : calls the remove_updates function. Run when the data has been updated

        SCHEDULER instance is run in another thread with with the Kthread class.

        Sched event names are added to a list of dictionary's, ACTIVE_SCHEDS, so that the
        threads can be terminated of the user cancles an update

    Arguments:

        update_interval {int} : integer value showing the number of seconds until the update function is run from the sched object

        update_name {str} : string containing the name of the update

        repeat {bool} : boolean stating whether the update will repeat every 24 hours or not

        update_type {str} : string which states whether the update will update news, covid data or news and covid data

        update_time {str} : string containing the time update function will be run

    Returns:

        None
    """
    sched_name = update_name

    log = 'NEWS UPDATE SCHED INSTANCE,', update_name, ', RUNNING FOR', update_interval, 'SECONDS UNTIL', update_time
    logging.info(log)

    if repeat:
        repeat_sched = SCHEDULER.enter(update_interval, 1, repeat_update, (update_type, update_name, update_time))
        logging.info('EVERY 24 HOURS')

    update_name = update_name+'news'
    update_name = SCHEDULER.enter(update_interval, 2, update_news_articles, ())

    cancel_sched = sched_name+'news_cancel'
    cancel_sched = SCHEDULER.enter(update_interval, 3, remove_update, (sched_name, global_vars.retrieve_updates(), False))

    news_thread = KThread(target=SCHEDULER.run)
    news_thread.start()

    ACTIVE_SCHEDS.append({
                        'sched_name' : sched_name, # acts as primary key
                        'sched' : update_name,
                        'cancel_sched' : cancel_sched,
                        'thread_name' : news_thread
    })

    return ACTIVE_SCHEDS

def update_news_articles() -> None:
    """
    Description:

        Function which updates the global variable articles with new covid data by calling the update_news function

    Arguments:

        None

    Returns:

        None
    """
    global_vars.update_articles(update_news(global_vars.retrieve_articles(), config['news_search_terms']))
    logging.info('NEWS UPDATED')


def get_interval(update_time:str) -> int:
    """
    Description:

        function to get the time interval for sched function

    Arguments:

        update_time {str} : string containing the time the update is meant to run

    Returns:

        seconds_unit_update {int} : integer stating seconds until the update
    """
    update_time = str(update_time)

    current_time = str(datetime.now())

    current_time_hour = int(current_time[11:13])
    current_time_minute = int(current_time[14:16])
    current_time_second = int(current_time[17:19])

    update_time_hour = int(update_time[0:2])
    update_time_minute = int(update_time[3:5])

    # gets time until next update
    seconds_until_update = time_difference(current_time_hour, current_time_minute, current_time_second, update_time_hour, update_time_minute)

    return seconds_until_update


def time_difference(h1:int, m1:int, s1:int, h2:int, m2:int, s2:int=0) -> int:
    """
    Description:

        function get difference between 2 times times

    Arguments:

        h1 {int} : integer which contains the value of the current hour

        m1 {int} : integer which contains the value of the current minute

        s1 {int} : integer which contains the value of the current second

        h2 {int} : integer which contains the value of the update hour

        m2 {int} : integer which contains the value of the update minute

        s2 {int} : integer which contains the value of the update second. 0 by default.

    Returns:

        diff {int} : the difference in seconds between teh current time and the update time
    """
    # convert h1 : m1 : s1 into seconds
    t1 = h1 * 3600 + m1 * 60 + s1

    # convert h2 : m2 : s2 into seconds
    t2 = h2 * 3600 + m2 * 60 + s2

    if t1 == t2:
        logging.warning("UPDATE TIME IS NOW")
        return 0

    # calculating the difference in secs
    diff = t2-t1

    if diff < 0:
        # calculates difference in seconds if s2 is before s1
        diff = 60 * 60 * 24 + diff

    return diff


def append_updates_list(update_type:str, repeat:bool, update_name:str, update_time:str, seconds_until_update:int) -> None:
    """
    Description:

        Function to append update information in a dictionary to global updates list

    Arguments:

        update_type {str} : string which states whether the update will update news, covid data or news and covid data

        repeat {bool} : boolean stating whether the update will repeat every 24 hours or not

        update_name {str} : string containing the name of the update

        update_time {str} : string containing the time the update is meant to run

        seconds_until_update {int} : integer value containing the number of seconds until the update

    Returns:

        None
    """
    if update_type == 'cn':

        log = 'COVID DATA AND NEWS UPDATE SCHEDULED FOR', seconds_until_update, 'SECONDS'
        logging.info(log)

        update_words = 'covid stats and news articles'
        schedule_covid_updates(seconds_until_update, update_name, repeat, update_type, update_time)
        schedule_news_updates(seconds_until_update, update_name, repeat, update_type, update_time)

    elif update_type == 'c':

        log = 'COVID DATA UPDATE SCHEDULED FOR', seconds_until_update, 'SECONDS'
        logging.info(log)

        update_words = 'covid stats'
        schedule_covid_updates(seconds_until_update, update_name, repeat, update_type, update_time)

    elif update_type == 'n':

        log = 'NEWS UPDATE SCHEDULED FOR', seconds_until_update, 'SECONDS'
        logging.info(log)

        update_words = 'news articles'
        schedule_news_updates(seconds_until_update, update_name, repeat, update_type,update_time)

    if repeat:
        repeats = ' It does this very 24 hours.'
    else:
        repeats = ''

    dictionary_to_add = {
                        'title' : update_name,
                        'content' : 'Updates '+update_words+' at '+update_time+'.'+repeats,
                        'update_time' : update_time,
                        'update_type' : update_type,
                        'repeat' : repeat
                        }

    # appends to list of updates
    updates = global_vars.retrieve_updates()
    updates.append(dictionary_to_add)
    global_vars.update_updates(updates)


def name_in_use(update_name:str) -> bool:
    """
    Description:

        Function to check if the update name has been used before

    Arguments:

        update_name {str} : string containing the name of the update

    Returns:

        None
    """
    if find_dictionary_key(update_name, 'title', 'title', global_vars.retrieve_updates()):
        return True
    return


def find_dictionary_key(query_data:any, search_key:str, key_to_find:str, list:list) -> any:
    """
    Description:

        Function to find a dictionary keys data in a list based on another dictionary keys data.

    Arguments:

        query_data {any} : the data you start off with within one of the dictionaries withon the list

        search_key {str} : string containing the name of the key which contains the query_data

        key_to_find {str} : string containing the name of the key containing the daa we want to find

        list {list} : the list of dictionaries being queried

    Returns:

        return_data {any} : the data which is linked to the key_to_find key
    """
    return_data = False

    x = 0
    for i in list:
        if list[x][search_key] == query_data:
            return_data =  list[x][key_to_find]
            break

        return_data = False

        x = x + 1

    return return_data


def remove_update(update_name:str, updates:list, remove_both:bool=True) -> list:
    """
    Description:

        Function to remove updates form the update list and unschedule if the user has clicked the "x" on a news article

    Arguments:

        update_name {str} : string containing the name of the update

        updates {list} : list containing all updates that are going to happen

        remove_both {bool} : booelan value which states whether news and covid data update is
            being removed or just news or covid data update

    Returns:

        updates {list} : list containing the updates without the updates which was just removed
    """
    # Cancels the update from schedular
    if remove_both:
        update_type = find_dictionary_key(update_name, 'title', 'update_type', global_vars.retrieve_updates())

        # runs stop thread and remove sched twice as there  are 2 threads with that name running
        if update_type == 'cn':
            stop_thread(update_name)
            stop_thread(update_name)

            remove_sched(update_name)
            remove_sched(update_name)

            log = '(1)CN SCHEDULER INSTANCES:"'+update_name+'","'+update_name+'" REMOVED'
            logging.info(log)

        elif update_type == 'c':
            stop_thread(update_name)

            remove_sched(update_name)

            log = '(1)C SCHEDULER INSTANCE:"'+update_name+'" REMOVED'
            logging.info(log)

        elif update_type == 'n':
            stop_thread(update_name)

            remove_sched(update_name)

            log = '(1)N SCHEDULER INSTANCE:"'+update_name+'" REMOVED'
            logging.info(log)
    else:
        log = '(2)SCHEDULER INSTANCE:"'+ update_name+ '" REMOVED'
        logging.info(log)


    # Removes from update list
    # cycles through each update in the list and removes it once the name has been found
    x = 0
    for i in updates:
        if updates[x]['title'] == update_name:
            updates.pop(x)
            break
        x = x + 1

    return updates


def remove_sched(update_name:str) -> None:
    """
    Description:

        function to remove sched instance from sched list

    Arguments:

        update_name {str} : string containing the name of the active sched

    Returns:

        None
    """
    x = 0
    for i in ACTIVE_SCHEDS:
        if ACTIVE_SCHEDS[x]['sched_name'] == update_name:
            ACTIVE_SCHEDS.pop(x)
        x = x + 1


def stop_thread(update_name:str) -> None:
    """
    Description:

        Function which stops a thread based on it's name. Uses the KThread Class to kill the thread.

    Arguments:

        update_name {str} : string containing the name of the update in the ACTIVE_SCHEDS list of dictionaries

    Returns:

        None
    """
    thread = find_dictionary_key(update_name, 'sched_name', 'thread_name', ACTIVE_SCHEDS)

    thread.kill() # kills the thread


class KThread(threading.Thread):
    """
    A subclass of threading.Thread, with a kill() method.

    This sub-class is from:
    https://web.archive.org/web/20130503082442/http:/mail.python.org/pipermail/python-list/2004-May/281943.html
    """
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run # Force the Thread to install our trace.
        threading.Thread.start(self)

    def __run(self):
        """Hacked run function, which installs the trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True

def repeat_update(update_type:str, update_name:str, update_time:str) -> None:
    """
    Description:

        Function called to repeat an update if repeat is set to True when creating an update.
        It will update again in 24 hours.

    Arguments:

        update_type {str} : string which states whether the update will update news, covid data or news and covid data

        update_name {str} : string containing the name of the update

        update_time {str} : string containing the time the update is meant to run

    Returns:

        None
    """
    append_updates_list(update_type, True, update_name, update_time, 86400)

    log = 'UPDATE:', update_name, ',WILL REPEAT IN 24 HOURS'
    logging.info(log)
