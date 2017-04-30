import requests
import threading
import datetime


class ApiRequests(threading.Thread):
    def __init__(self, url, collection):
        threading.Thread.__init__(self)
        self.updated = 0
        self.url = url
        self.collection = collection

    def run(self):
        change_id = requests.get('http://api.poe.ninja/api/Data/GetStats').json()['nextChangeId']
        while 1:
            response = self.make_json_request(change_id)
            #print(change_id)
            change_id = response['next_change_id']
            self.add_to_db(self.collection, response['stashes'])

    def make_json_request(self, change_id):
        r = requests.get(self.url, {'id': change_id})
        poe_data = r.json()
        return poe_data

    def add_to_db(self, collection, stashes):
        for stash in stashes:
            stash['updated_time'] = datetime.datetime.now()
            update = collection.replace_one({'id': stash['id']}, stash, True)
            self.updated += update.modified_count
        return self.updated
