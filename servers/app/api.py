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
import os
from email.mime.text import MIMEText
from smtplib import SMTP

from app.end_points import users,auth,utils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
api_router = APIRouter()

api_router.include_router(users.router, prefix = "/api/user",tags = ["user"])
api_router.include_router(auth.router,prefix = "/api/auth",tags = ["auth"])
api_router.include_router(utils.router,prefix = "/api/util",tags = ["util"])

