from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from models.user import EmailCode, User, JWT
from services.mailcodeservice import generate_code, send_email
from motor.motor_asyncio import AsyncIOMotorClient
import datetime
from config.database import get_db

router = APIRouter()


@router.post("/email/", status_code=status.HTTP_201_CREATED)
async def create_user(data: User, db: AsyncIOMotorClient = Depends(get_db)):
    existing_code = db.users_collection.find_one({"email": data.email, "expiration": {"$gt": datetime.datetime.now()}})

    if existing_code:
        raise HTTPException(status_code=404, detail="Code exists")
    else:
        code = generate_code()
        expiration = datetime.datetime.now() + datetime.timedelta(minutes=30)
        result = db.users_collection.insert_one({"code": code, "email": data.email, "expiration": expiration, "tries": 0})
        send_email(data.email, code)

    payload = {"message": "User account has been successfully created. Check your email for verification code."}
    return JSONResponse(content=payload)


@router.get("/verify/", status_code=status.HTTP_200_OK)
async def check_code(
    email: str = Query(..., description="User email"),
    code: str = Query(..., description="Verification code"),
    db: AsyncIOMotorClient = Depends(get_db)
):

    users_collection = db["users_collection"]
    user = users_collection.find_one({"email": email, "expiration": {"$gt": datetime.datetime.now()}})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user["code"] != code:
        users_collection.update_one({"email": email}, {"$inc": {"tries": 1}})

        if user["tries"] >= 3:

            new_code = generate_code()
            expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=30)

            await users_collection.update_one(
                {"email": email},
                {"$set": {"code": new_code, "tries": 0, "expiration": expiration_time}}
            )
            send_email(email, new_code)
            return {"message": "Code sent. Please check your email for the new code."}

        raise HTTPException(status_code=422, detail="Incorrect code. Please try again.")

    if user["expiration"] < datetime.datetime.now():
        raise HTTPException(status_code=422, detail="Code has expired. Please request a new one.")

    return {"message": "Code is valid."}
