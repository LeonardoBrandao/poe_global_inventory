import requests
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client.poe_test
collection = db.stashes


r = requests.get('http://www.pathofexile.com/api/public-stash-tabs')
poe_data = r.json()

stashes = poe_data['stashes']
old_change_id = poe_data['next_change_id']
collection.insert_many(stashes)
params = {'id': '64117986-67657799-63387716-73647014-68452700'}
updated = 0

while True:
    r = requests.get('http://www.pathofexile.com/api/public-stash-tabs', params=params)
    poe_data = r.json()
    print("="*10+old_change_id+"="*10)
    print(updated)
    if old_change_id is not poe_data['next_change_id']:
        stashes = poe_data['stashes']
        old_change_id = poe_data['next_change_id']
        for stash in stashes:
            update = collection.replace_one({'id': stash['id']}, stash, True)
            updated += update.modified_count
        params = {'id': old_change_id}
    else:
        break
