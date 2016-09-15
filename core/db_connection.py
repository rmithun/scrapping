"""python file to establish db connection with mongodb"""

from pymongo import MongoClient

from .config import (
    DB_NAME,
    CROWD_COLLECTION,
    KICKSTART_COLLECTION
)

client = MongoClient()
client = MongoClient('localhost', 27017)

DATABASE = client[DB_NAME]
CROWD_CUBE_COLLECTION = DATABASE[CROWD_COLLECTION]
KICK_START_COLLECTION = DATABASE[KICKSTART_COLLECTION]
