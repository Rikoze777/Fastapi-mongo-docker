from fastapi import FastAPI
from routes.mail_router import router as mail_router

app = FastAPI()

app.include_router(mail_router, tags=["mailsend"])
