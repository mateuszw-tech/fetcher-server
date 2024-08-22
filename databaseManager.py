from pymongo import MongoClient
#
# client = MongoClient('localhost', 27017)
#
# db = client.test
#
# test = db.test
#
# mike = test.insert_one({'name': 'Mike', 'age': 23})
#
# anna = test.insert_one({'name': 'Anna', 'age': 23})


class DatabaseManager:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.webscraper
        self.collection = self.db.osintData

    def insert_data_to_database(self, data_json):
        self.collection.insert_one(data_json)

    def find_data_from_database_by_phone_number(self, phone_number):
        print([advertisement for advertisement in self.collection.find({'phone_number': phone_number})])
