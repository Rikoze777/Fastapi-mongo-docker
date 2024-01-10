from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    email: EmailStr


class JWT(BaseModel):
    email: EmailStr
    expiration: datetime = None


class EmailCode(BaseModel):
    code: str
    email: EmailStr
    expiration: datetime = None
    tries: int
