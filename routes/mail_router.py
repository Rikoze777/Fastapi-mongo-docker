from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from models.user import EmailCode, User, JWT
from services.mailcodeservice import generate_code, send_email
from motor.motor_asyncio import AsyncIOMotorClient
import datetime
from config.database import get_db
from services.user import create_user_account

router = APIRouter()


@router.post("/email/", status_code=status.HTTP_201_CREATED)
async def create_user(data: User, db: AsyncIOMotorClient = Depends(get_db)):
    existing_code = db.users_collection.find_one({"email": data.email, "expiration": {"$gt": datetime.datetime.utcnow()}})

    if existing_code:
        return existing_code
    else:
        code = generate_code()
        expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        result = db.users_collection.insert_one({"code": code, "email": data.email, "expiration": expiration, "tries": 0})
        await send_email(data.email, code)

    payload = {"message": "User account has been successfully created. Check your email for verification code."}
    return JSONResponse(content=payload)


# @router.post("/validate/", response_model=dict)
# async def validate_code(email_code: EmailCode, db: AsyncIOMotorClient = Depends(database)):
#     # Check if the provided code matches the stored code in the database
#     stored_code = await db.users_collection.find_one({"email": email_code.email, "expiration": {"$gt": datetime.utcnow()}})
    
#     if stored_code and stored_code["code"] == email_code.code:
#         # Increment the tries
#         tries = stored_code["tries"] + 1

#         # Check if the user has tried three times
#         if tries >= 3:
#             # If the user has tried three times, delete the code
#             await db.email_codes.delete_one({"_id": stored_code["_id"]})
#         else:
#             # If the user hasn't tried three times, update the tries
#             await db.email_codes.update_one({"_id": stored_code["_id"]}, {"$set": {"tries": tries}})
        
#         return {"message": "Code validation successful"}
#     else:
#         raise HTTPException(status_code=400, detail="Invalid code or expired")