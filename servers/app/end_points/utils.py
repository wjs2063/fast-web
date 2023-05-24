from fastapi import *
from fastapi.responses import *
from typing import Annotated
from models.database import *
from schemas.token import *
from fastapi.staticfiles import StaticFiles
from configs.constant import *
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime,timedelta
from schemas.userSchema import *
from bson import ObjectId
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from schemas.emailSchema import *
import os
from email.mime.text import MIMEText
from smtplib import SMTP



router = APIRouter()


@router.post("/email")
async def send_email(body: EmailSchema):
    try:
        msg = MIMEText(body.message, "html")
        msg['Subject'] = body.subject
        msg['From'] = f'CODE PLANET <{OWN_EMAIL}>'
        msg['To'] = body.to

        port = 587  # For SSL

        # Connect to the email server
        server = SMTP("smtp.naver.com", port)
        server.starttls()
        server.login(OWN_EMAIL, OWN_EMAIL_PASSWORD)

        # Send the email
        server.send_message(msg)
        server.quit()
        return {"message": "Email sent successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)