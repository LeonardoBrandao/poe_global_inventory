import requests
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client.poe_test
collection = db.stashes

updated_change_id = requests.get('http://api.poe.ninja/api/Data/GetStats').json()['nextChangeId']
params = {'id': updated_change_id}
updated = 0

while True:
    r = requests.get('http://www.pathofexile.com/api/public-stash-tabs', params=params)
    poe_data = r.json()
    print("="*10+params['id']+"="*10)
    print(updated)
    stashes = poe_data['stashes']
    for stash in stashes:
        update = collection.replace_one({'id': stash['id']}, stash, True)
        updated += update.modified_count
    params = {'id': poe_data['next_change_id']}
