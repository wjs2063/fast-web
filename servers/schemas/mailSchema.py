from pydantic import BaseModel,EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from configs.constant import *
from typing import List
class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME = OWN_EMAIL,
    MAIL_PASSWORD = OWN_EMAIL_PASSWORD,
    MAIL_FROM = OWN_EMAIL,
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.naver.com",
    MAIL_FROM_NAME="CODE PLANET",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)
