import random
import smtplib
from config.config import Config


config = Config()

MAIL_FROM = config.MAIL_FROM
MAIL_PASSWORD = config.MAIL_PASSWORD


def send_email(mail_to, code):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(MAIL_FROM, MAIL_PASSWORD)
    message = 'Subject: {}\n\n{}'.format('Code', code)
    server.sendmail(MAIL_FROM, mail_to, message)
    print('Email sent successfully')
    server.quit()


def generate_code():
    return str(random.randint(100000000000, 999999999999))
