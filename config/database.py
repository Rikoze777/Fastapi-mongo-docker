import motor.motor_asyncio
from bson.objectid import ObjectId
from schema.schemas import individual_user

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.users_db

user_collection = database.get_collection("users_collection")


async def add_user(student_data: dict) -> dict:
    user = await user_collection.insert_one(student_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return individual_user(new_user)


async def delete_user(id: str):
    student = await user_collection.find_one({"_id": ObjectId(id)})
    if student:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True
