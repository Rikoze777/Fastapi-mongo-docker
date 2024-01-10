from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from models.user import EmailCode, User, JWT
from services.mailcodeservice import generate_code, send_email
from motor.motor_asyncio import AsyncIOMotorClient
import datetime
from config.database import get_db

router = APIRouter()


@router.post("/email/", status_code=status.HTTP_201_CREATED)
async def create_user(data: User, db: AsyncIOMotorClient = Depends(get_db)):
    existing_code = db.users_collection.find_one({"email": data.email, "expiration": {"$gt": datetime.datetime.utcnow()}})

    if existing_code:
        return existing_code # Переделать и отправлять рейз ошибки
    else:
        code = generate_code()
        expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        result = db.users_collection.insert_one({"code": code, "email": data.email, "expiration": expiration, "tries": 0})
        await send_email(data.email, code)

    payload = {"message": "User account has been successfully created. Check your email for verification code."}
    return JSONResponse(content=payload)

