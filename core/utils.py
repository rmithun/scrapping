"""common utils"""


def store_data(data, collection):
    """function which creates a db connection and stores the data passed"""
    # save data
    try:
        for item in data:
            collection.insert(item)
        return True
    except Exception as e:
        print(repr(e))
        return False
