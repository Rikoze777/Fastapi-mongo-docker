from bson import ObjectId
from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    id: ObjectId
    email: EmailStr


class JWT(BaseModel):
    email: EmailStr
    id: ObjectId
    expiration: datetime = None


class EmailCode(BaseModel):
    code: str
    email: EmailStr
    expiration: datetime = None
    tries: int
