from fastapi import APIRouter, Depends, HTTPException
from models.user import EmailCode, User, JWT
from services.mailcodeservice import generate_code, send_email
from motor.motor_asyncio import AsyncIOMotorClient
import datetime
from config.database import database

router = APIRouter()


@router.post("/email/", response_model=EmailCode)
async def request_code(user: User, db: AsyncIOMotorClient = Depends(database)):
    # Check if there's an existing code for the user
    existing_code = await db.users_collection.find_one({"email": user.email, "expiration": {"$gt": datetime.utcnow()}})
    
    if existing_code:
        # If there's an existing code, return it
        return existing_code
    else:
        # Generate a 12-symbol code
        code = generate_code()

        # Set expiration time (adjust the timedelta as needed)
        expiration = datetime.utcnow() + datetime.timedelta(minutes=15)

        # Insert the code into the MongoDB collection
        result = await db.users_collection.insert_one({"code": code, "email": user.email, "expiration": expiration, "tries": 0})

        # Send the code to the user via email
        await send_email(user.email, code)

        return EmailCode(code=code, email=user.email, expiration=expiration, tries=0)


@router.post("/validate/", response_model=dict)
async def validate_code(email_code: EmailCode, db: AsyncIOMotorClient = Depends(database)):
    # Check if the provided code matches the stored code in the database
    stored_code = await db.users_collection.find_one({"email": email_code.email, "expiration": {"$gt": datetime.utcnow()}})
    
    if stored_code and stored_code["code"] == email_code.code:
        # Increment the tries
        tries = stored_code["tries"] + 1

        # Check if the user has tried three times
        if tries >= 3:
            # If the user has tried three times, delete the code
            await db.email_codes.delete_one({"_id": stored_code["_id"]})
        else:
            # If the user hasn't tried three times, update the tries
            await db.email_codes.update_one({"_id": stored_code["_id"]}, {"$set": {"tries": tries}})
        
        return {"message": "Code validation successful"}
    else:
        raise HTTPException(status_code=400, detail="Invalid code or expired")