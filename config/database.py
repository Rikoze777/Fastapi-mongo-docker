from pymongo.mongo_client import MongoClient
from environs import Env


env = Env()
env.read_env()
uri = env('MONGO_URI')

client = MongoClient(uri)

db = client.mongo_db
user_collection = db["user_collection"]
