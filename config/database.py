from typing import Generator
from pymongo import MongoClient
from pymongo.collection import Collection
from environs import Env


env = Env()
env.read_env()

MONGO_USERNAME = env.str("MONGO_USERNAME")
MONGO_PASSWORD = env.str("MONGO_PASSWORD")
MONGO_DB = env.str("MONGO_DB")

MONGO_DETAILS = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@0.0.0.0:27017/{MONGO_DB}"

client = MongoClient(MONGO_DETAILS)
database = client[MONGO_DB]
users_collection: Collection = database["users"]


def get_db() -> Generator:
    try:
        yield users_collection
    finally:
        pass
