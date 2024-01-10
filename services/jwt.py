import datetime
from config.config import Config
from jose import jwt

config = Config()


def create_jwt_token(data: dict):
    expiration = datetime.datetime.now() + datetime.timedelta(minutes=30)
    to_encode = data.copy()
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt, expiration
