from pymongo import MongoClient
import datetime

class SearchMongo:
    def __init__(self, db):
        self.db = db

    def get_poe_stashes(self):
        return self.db.stashes

    def search_unique(self, itemname, time):
        result = self.db.stashes.aggregate([
            {'$match': {
                '$and': [{'items.name': '<<set:MS>><<set:M>><<set:S>>Tabula Rasa'}, {'updated_time': {'$gt': time}}]}},
            {'$project': {'items': {'$filter': {'input': '$items',
                                                'as': 'item',
                                                'cond': {
                                                    '$eq': ['$$item.name', '<<set:MS>><<set:M>><<set:S>>'+itemname]}
                                                }
                                    }
                          }
             }
        ])
        return list(result)
