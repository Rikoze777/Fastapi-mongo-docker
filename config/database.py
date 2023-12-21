from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from schema.schemas import individual_user
from environs import Env


env = Env()
env.read_env()

MONGO_USERNAME = env.str("MONGO_USERNAME")
MONGO_PASSWORD = env.str("MONGO_PASSWORD")
MONGO_DB = env.str("MONGO_DB")

MONGO_DETAILS = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@mongo:27017/{MONGO_DB}"

client = AsyncIOMotorClient(MONGO_DETAILS)

database = client.get_database(MONGO_DB)

users_collection = database.get_collection("users_collection")


async def add_user(user_data: dict) -> dict:
    user = await users_collection.insert_one(user_data)
    new_user = await users_collection.find_one({"_id": user.inserted_id})
    return individual_user(new_user)


async def delete_user(id: str):
    student = await users_collection.find_one({"_id": ObjectId(id)})
    if student:
        await users_collection.delete_one({"_id": ObjectId(id)})
        return True


def get_user_by_email(email: str):
    return users_collection.find_one({"email": email})