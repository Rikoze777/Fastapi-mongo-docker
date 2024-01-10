from typing import Generator
from pymongo import MongoClient
from pymongo.collection import Collection
from config.config import Config


config = Config()
MONGO_USERNAME = config.MONGO_USERNAME
MONGO_PASSWORD = config.MONGO_PASSWORD
MONGO_DB = config.MONGO_DB
MONGO_IP = config.MONGO_IP

MONGO_DETAILS = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_IP}:27017/{MONGO_DB}"

client = MongoClient(MONGO_DETAILS)
database = client[MONGO_DB]
users_collection: Collection = database["users"]


def get_db() -> Generator:
    try:
        yield users_collection
    finally:
        pass
