from pymongo import MongoClient
from ApiRequests import ApiRequests
from SearchMongo import SearchMongo
import time
import datetime

if __name__ == '__main__':

    client = MongoClient('mongodb://localhost:27017/')
    db = client.poe_test
    collection = db.stashes

    se = SearchMongo(db)

    request = ApiRequests("http://www.pathofexile.com/api/public-stash-tabs", collection)

    request.start()
    now = datetime.datetime.now()

    time.sleep(10)

    while 1:
        results = se.search_unique('Tabula Rasa', now)
        if len(results) >= 1:
            now = datetime.datetime.now()
            print(results)
        time.sleep(1)
