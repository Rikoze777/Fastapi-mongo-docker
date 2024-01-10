from pydantic_settings import BaseSettings


class Config(BaseSettings):
    MONGO_URI: str
    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGO_DB: str
    MAIL_FROM: str
    MAIL_PASSWORD: str
    MONGO_DETAILS: str
    MONGO_IP: str
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = "../.env"
