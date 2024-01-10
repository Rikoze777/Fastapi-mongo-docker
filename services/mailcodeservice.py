import random
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from config.config import Config

config = Config()

MAIL_FROM = config.MAIL_FROM
MAIL_USERNAME = config.MAIL_USERNAME
MAIL_PASSWORD = config.MAIL_PASSWORD

mail_conf = ConnectionConfig(
    # MAIL_USERNAME = MAIL_USERNAME,
    MAIL_PASSWORD = MAIL_PASSWORD,
    MAIL_FROM = MAIL_FROM,
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.yandex.ru",
    MAIL_FROM_NAME="mailserver",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = False,
)

fastmail = FastMail(mail_conf)


async def send_email(email: str, code: str):
    message = MessageSchema(
        subject="Your Verification Code",
        recipients=[email],
        body=f"Your verification code is: {code}",
        subtype=MessageType.html
    )
    await fastmail.send_message(message)


def generate_code():
    return str(random.randint(100000000000, 999999999999))
