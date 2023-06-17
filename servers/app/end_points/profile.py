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
from models.database import *
from configs.security import *
from schemas.question_schema import *
from fastapi.encoders import jsonable_encoder
from models.crud import *
from configs.status_code import *
import json

router = APIRouter()

# user_id 의 질문목록 가져오기 
@router.get("/question-list",responses = {**response_status_code})
async def get_question_list(request: Request,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)],access_token : str =  Header()):
    req = dict(request)
    req = convert_binary_to_string(req)
    # token 검증 ( refresh + access)
    verfiy_token(req = req,access_token = access_token)
    # access_token 복호화
    decoded_access_token = decode_jwt_token(token = access_token)
    # userId 의 질문총개수 
    total_docs = await count_total_documents(db = db,collection = QUESTIONS,query = {USER_ID:decoded_access_token.get(USER_ID)})
    # 10개씩 끊어서 가져온다(제일 첫페이지 10개)
    questions = await find_many_with_pagination(db = db,collection = QUESTIONS,query = {USER_ID :decoded_access_token.get(USER_ID)})
    # List[class] 형태에서 class 내부 변수가 ObjectId 일때 serealize 하는 pydantic 코드를 찾아야함.
    response = JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {
            TOTAL_DOCS : total_docs,
            QUESTIONS : jsonable_encoder(serealize(questions))
        }
        )
    return response