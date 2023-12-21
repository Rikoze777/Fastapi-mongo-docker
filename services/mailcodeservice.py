import random
from environs import Env
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema


env = Env()
env.read_env()

MAIL_FROM = env.str("MAIL_FROM")
MAIL_USERNAME = env.str("MAIL_USERNAME")
MAIL_PASSWORD = env.str("MAIL_PASSWORD")

conf = ConnectionConfig(
    MAIL_USERNAME = MAIL_USERNAME,
    MAIL_PASSWORD = MAIL_PASSWORD,
    MAIL_FROM = MAIL_FROM,
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.yandex.ru",
    MAIL_FROM_NAME="Riko",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

fastmail = FastMail(conf)


async def send_email(email: str, code: str):
    message = MessageSchema(
        subject="Your Verification Code",
        recipients=[email],
        body=f"Your verification code is: {code}",
        subtype="html"
    )
    await fastmail.send_message(message)


def generate_code():
    return str(random.randint(100000000000, 999999999999))
