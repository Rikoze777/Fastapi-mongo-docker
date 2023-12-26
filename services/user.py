from fastapi import HTTPException

from models.user import User


async def create_user_account(data, db):
    user = db.find_one({"email": data.email})
    if user:
        raise HTTPException(status_code=422, detail="Email is already registered with us.")

    new_user = User(
        email=data.email,
    )
    new_user = dict(new_user)
    db.users_collection.insert_one(new_user)
    return new_user