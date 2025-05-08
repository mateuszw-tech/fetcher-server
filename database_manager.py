from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class DatabaseManager:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.webscraper
        self.collection = self.db.osintData

    def insert_advertisement_info_to_database(self, data_json):
        try:
            self.collection.insert_one(data_json)
        except DuplicateKeyError:
            pass

    def return_advertisement_in_db_by_phone_number(self, phone_number):
        return [advertisement for advertisement in self.collection.find({'phone_number': phone_number})]
