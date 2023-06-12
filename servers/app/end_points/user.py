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
from models.database import *
from configs.security import *


router = APIRouter()

# user_id 의 질문목록 가져오기 
@router.get("/question/{user_id}")
async def get_question_list(db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)],access_token : str =  Header()):
    pass
    

# user_id 의 질문 등록 
@router.post("/question/{user_id}")
async def post_question(user_id,question,request:Request,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)],access_token : str =  Header()):
    decoded_access_jwt = decode_jwt_token(access_token)
    # 로그인용 토큰 check
    verify_usage(decoded_token = decoded_access_jwt,usage = "login")
    # user_id check
    verify_user_id(decoded_token = decoded_access_jwt,user_id = user_id)
    req = dict(request)
    req = convert_binary_to_string(req)
    cookies = parse_cookie(req)
    # refresh_token 이없으면 login_required 
    if not cookies.get("refresh_token"):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail = "Login Required")

    

# user_id 의 question 의 질문 수정
@router.put("/question/{user_id}")
async def update_question(db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)],access_token : str =  Header()):
    pass

# user_id 의 question 삭제
@router.delete("/question/{user_id}")
async def update_question(db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)],access_token : str =  Header()):
    pass
 
