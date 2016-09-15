"""Functions to scrap and store the scrapped data from kickstarter api"""

# python imports
import requests
import re
import datetime

from bs4 import BeautifulSoup

from .db_connection import KICK_START_COLLECTION
from .config import PITCH_CATEGORY, API_URL
from .utils import store_data

headers = {'Accept': 'application/json, text/javascript'}

URL = 'https://www.kickstarter.com/discover/categories/{}'.format(
    PITCH_CATEGORY)


def fetch_data_from_api():
    """function which fetchs data from the give url and stores it
    """
    link = requests.get(URL)
    page = 1
    data = []
    if link.status_code == 200:
        soup = BeautifulSoup(link.content, "lxml")
        category_id = soup.find(
            'li', {'class':
                   'category selected'}).find('a')['data-id']
        while len(data) < 100:
            json_link = requests.get(
                API_URL.format(int(category_id), page), headers=headers)
            if json_link.status_code:
                current_data_len = 100 - len(data)
                data.extend(json_link.json()['projects'][:current_data_len])
                page += 1
            else:
                break
        has_saved = store_data(data, KICK_START_COLLECTION)
        if data:
            print("\n \nSuccessfully updated kickstarter scrapped data")
    else:
        print("The given category not found")
