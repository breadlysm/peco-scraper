import datetime
from urllib.parse import urlunsplit, urlencode
import re
import os
import json
from utils.logger import info, error, debug
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

START_DATE = os.environ.get('START_DATE')


def get_today():
    today = datetime.datetime.now().isoformat()
    return today

def wait_until_exists(driver,element):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, element)))
    finally:
        info('Found Element')
        return driver.find_element_by_xpath(element)


def find_inputs(driver, name):
    # loops all inputs
    for input in driver.find_elements_by_tag_name('input'):
        # Matches the element name with the Passed argument
        if input.get_property('name') == name:
            # Attempts to interact with element. If impossible, find next
            try:
                input.clear()
            except:
                continue
            info('Found ' + name + ' input')
            return input


def to_timestamp(start):
    timestamp = datetime.datetime.strptime(start, "%Y-%m-%d").isoformat()
    return timestamp


def api_url(account_id, start=to_timestamp(START_DATE),
            end=get_today(),
            agg_type='hour'):

    scheme = 'https'
    netloc = 'peco.opower.com'
    path = f"/ei/edge/apis/DataBrowser-v1/cws/cost/utilityAccount/{account_id}"
    query = urlencode(
        dict(startDate=start, endDate=end, aggregateType=agg_type))
    url = urlunsplit((scheme, netloc, path, query, ""))
    return url


def get_uuid(txt):
    return re.findall(r"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b", txt)[0]


def days_to_seconds(days):
    return (24*60*60*days)

def hours_to_seconds(hours):
    return (hours*60*60)

def timestamp_to_iso(timestamp):
    dt = datetime.datetime
    return dt.fromtimestamp(timestamp).isoformat()

def iso_to_timestamp(timestamp):
    return datetime.datetime.fromisoformat(timestamp)