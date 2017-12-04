"""demo file"""


from core.scrapper import scrap_crowdcube
from core.analyse_data import (
    find_total_amount_raised,
    find_total_amount_raised_using_aggregate)
from core.api_scrapping import fetch_data_from_api

from core.db_connection import CROWD_CUBE_COLLECTION


# DEMO 1 WEB SCRAPPING
scrap_crowdcube()
# DEMO 2 Data analysis
find_total_amount_raised(CROWD_CUBE_COLLECTION)
find_total_amount_raised_using_aggregate(CROWD_CUBE_COLLECTION)
# DEMO 3 API
fetch_data_from_api()

