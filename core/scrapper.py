"""Functions to scrap and store the scrapped data from crowdcube"""

# python imports
import requests
import re
import datetime


# import the Beautiful soup functions to parse the data returned from the
# website
from bs4 import BeautifulSoup
from .db_connection import CROWD_CUBE_COLLECTION
from .utils import store_data


def scrap_crowdcube():
    """function which scraps the crowd cube website and stores the data"""
    link = requests.get('https://www.crowdcube.com/investments')
    soup = BeautifulSoup(link.content, "lxml")
    # parse the html and extract the content
    parsed_data = []
    today = datetime.datetime.today().date()
    pitches = soup.findAll("div", {"class": "pitch"})
    for pitch in pitches:
        pitch_dict = {}
        title_details = pitch.find('h2').find('a')
        link, title = title_details['href'], title_details['title'].strip()
        desciption = pitch.find(
            'p', {'class': 'pitch__description'}).text.strip()
        amount_raised = pitch.find(
            'span', {'class': 'pitchProgress__figure'}).text
        amount_raised = ''.join(x for x in amount_raised if x.isdigit())
        percentage_raised = pitch.find(
            'span', {'class': 'pitchProgress__percentage'}).text
        pitch_stat = pitch.findAll('li', {'class': 'pitch__stat'})
        pitch_figure = pitch_stat[3].find(
            'span', {'class': 'pitch__statFigure'})
        if pitch_figure:
            days_left = pitch_figure.text.strip()
        else:
            days_left = pitch_stat[3].find(
                'span', {'class': 'timeRemaining__figure'}).text.strip()
        if not days_left:
            days_left = 0
        pitch_dict = {
            'pitch_title': title, 'pitch_link': link,
            'pitch_summary': desciption,
            'amount_raised': int(amount_raised),
            'percentage_raised': int(re.search(r'\d+',
                                               percentage_raised).group()),
            'days_left': int(days_left),
            'day_updated': today.strftime('%Y-%m-%d')
        }
        parsed_data.append(pitch_dict)
    # save parsed content
    has_saved = store_data(parsed_data, CROWD_CUBE_COLLECTION)
    if has_saved:
        print("Successfully updated crowdcube scrapped data \n\n")
