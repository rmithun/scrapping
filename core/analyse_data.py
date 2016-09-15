"""function which is used to analyze the data from db"""
# python imports
import datetime

from .db_connection import CROWD_CUBE_COLLECTION, KICK_START_COLLECTION

TODAY = datetime.datetime.today().date().strftime('%Y-%m-%d')


def find_total_amount_raised(collection):
    """function to find total amount raised by a pitch
    which has atleast 10 days remaining"""
    print("Total amount raised -Pythonic way\n \n")
    pitch_data = {}
    total_amount_raised = 0
    for data in collection.find():
        if TODAY == data['day_updated']:
            if data['days_left'] > 0 and data['days_left'] <= 10:
                pitch_data[data['pitch_title']] = data['amount_raised']
                total_amount_raised = total_amount_raised + \
                    data['amount_raised']
                print(data['pitch_title'], data['amount_raised'])
    print("Total amount raised by all pitches {} \n".format(
        total_amount_raised))


def find_total_amount_raised_using_aggregate(collection):
    """function to find total amount raised using mongodb aggregate by a pitch
    which has atleast 10 days remaining"""
    print("Total amount raised - Mongodb aggregate method")
    cursor = collection.aggregate(
        [{"$match": {"day_updated": TODAY,
                     "days_left": {"$gt": 0, "$lt": 11}}}, {
            "$group": {"_id": "$pitch_title",
                       "amount_raised": {"$sum": "$amount_raised"},
                       "days_left": {"$sum": "$days_left"}}}])
    for item in cursor:
        print(item['_id'], item['amount_raised'])
