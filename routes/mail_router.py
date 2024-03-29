from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from models.user import User
from services.jwt import create_jwt_token
from services.mailcodeservice import generate_code, send_email
from motor.motor_asyncio import AsyncIOMotorClient
import datetime
from config.database import get_db
from services.user import get_current_user

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

    jwt_token, jwt_expiration = create_jwt_token({"sub": email})
    users_collection.update_one(
        {"email": email},
        {"$set": {"jwt": jwt_token, "jwt_expiration": jwt_expiration}}
    )
    return {"message": "Code is valid.", "jwt_token": jwt_token}


@router.get("/verify-jwt")
async def validate_jwt(token: str = Query(..., description="Paste your JWT token here"), db: AsyncIOMotorClient = Depends(get_db)):
    current_user = await get_current_user(token, db)

    if current_user["jwt_expiration"] < datetime.datetime.now():
        raise HTTPException(status_code=401, detail="JWT has expired")

    return {"id": str(current_user["_id"]), "email": current_user["email"]}
