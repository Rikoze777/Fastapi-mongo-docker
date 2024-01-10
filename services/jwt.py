import datetime
from config.config import SECRET_KEY, ALGORITHM
from jose import JWTError


def create_jwt_token(data: dict):
    # Function to create a JWT token
    expiration = datetime.utcnow() + datetime.timedelta(minutes=30)
    to_encode = data.copy()
    to_encode.update({"exp": expiration})
    encoded_jwt = JWTError.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
