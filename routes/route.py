from fastapi import APIRouter
from models.user import User
from config.database import user_collection
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()
