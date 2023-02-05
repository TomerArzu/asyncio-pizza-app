import logging
from dataclasses import asdict

import pymongo
from pymongo.collection import Collection

from const import MONGODB_CONNECTION_STRING, DATABASE_NAME, REPORTS_COLLECTION_NAME
from domian.repository import DatabaseRepository

logger = logging.getLogger("org.mongodb.driver")
logger.setLevel(logging.NOTSET)


class MongoDBRepository(DatabaseRepository):
    def __init__(self):
        self._client = None
        self._pizza_db = None
        self._report_collection: Collection = None
        self._establish_connection()
        self._get_reports_collection()

    def _establish_connection(self):
        self._client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)
        self._pizza_db = self._client[DATABASE_NAME]

    def _get_reports_collection(self):
        try:
            self._report_collection = self._pizza_db.create_collection(REPORTS_COLLECTION_NAME)
        except pymongo.errors.CollectionInvalid:
            self._report_collection = self._pizza_db.get_collection(REPORTS_COLLECTION_NAME)

    def update(self, document_filter, updated_data):
        ...

    def save(self, data):
        result = self._report_collection.insert_one(document=asdict(data))
        if result:
            print("document saved !  ")
        else:
            print("document lost :(  ")

    def delete(self, document_filter):
        pass

    def get(self):
        pass
