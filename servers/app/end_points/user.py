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

router = APIRouter()

# user_id 의 질문목록 가져오기 
@router.get("/question")
async def get_question_list(db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)],access_token : str =  Header()):
    pass
    

# user_id 의 질문 등록 
@router.post("/question",status_code = status.HTTP_201_CREATED,response_model = OutputQuestion)
async def post_question(question:Input_Question,request:Request,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)],access_token : str =  Header()):
    req = dict(request)
    req = convert_binary_to_string(req)
    # token validate
    verfiy_token(req,access_token = access_token)
    current_time = datetime.utcnow()
    question = question.dict()
    question[CREATED_AT] = current_time
    question[UPDATED_AT] = current_time
    _id = await insert_one(db = db ,collection = "questions",query = question)
    question[OBJECT_ID] = str(ObjectId(_id.inserted_id))
    question = OutputQuestion(**question)
    return question


    

# user_id 의 question 의 질문 수정
@router.put("/question")
async def update_question(db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)],access_token : str =  Header()):
    pass

# user_id 의 question 삭제
@router.delete("/question")
async def update_question(db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)],access_token : str =  Header()):
    pass
 
