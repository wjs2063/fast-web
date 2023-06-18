from fastapi import *
from fastapi.responses import *
from typing import Annotated
from models.database import *
from schemas.token_schema import *
from fastapi.staticfiles import StaticFiles
from configs.constant import *
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime,timedelta
from schemas.user_schema import *
from bson import ObjectId
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
import os
from email.mime.text import MIMEText
from smtplib import SMTP

from app.end_points import user,auth,util,profile,account,admin,board

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
api_router = APIRouter()

api_router.include_router(user.router, prefix = "/api/user",tags = ["user"])
api_router.include_router(auth.router,prefix = "/api/auth",tags = ["auth"])
api_router.include_router(util.router,prefix = "/api/util",tags = ["util"])
api_router.include_router(profile.router,prefix = "/api/profile",tags = ["profile"])
api_router.include_router(account.router,prefix = "/api/account",tags = ["account"])
api_router.include_router(admin.router,prefix = "/api/admin",tags = ["admin"])
api_router.include_router(board.router,prefix = "/api/board",tags = ["board"])



