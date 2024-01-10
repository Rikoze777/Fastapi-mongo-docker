from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from motor.motor_asyncio import AsyncIOMotorClient
from config.config import SECRET_KEY, ALGORITHM
from config.config import Config
from config.database import get_db


config = Config()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Security(oauth2_scheme), db: AsyncIOMotorClient = Depends(get_db)):
    # Function to get the current user from JWT token
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = JWTError.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db["users_collection"].find_one({"email": email})
    if user is None:
        raise credentials_exception

    return user
