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
from schemas.answer_schema import *
from configs.status_code import *
import json

router = APIRouter()



# 특정 question 가져오기
@router.get("/question",status_code = status.HTTP_200_OK,responses = {**response_status_code})
async def get_question(question_id:str,request:Request,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)],access_token : str =  Header()):
    pass

# user의 질문 등록 
@router.post("/question",status_code = status.HTTP_201_CREATED,response_model = OutputQuestion,responses = {**response_status_code})
async def post_question(question:Input_Question,request:Request,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)],access_token : str =  Header()):
    req = dict(request)
    req = convert_binary_to_string(req)
    # token validate
    verfiy_token(req,access_token = access_token)
    decoded_access_token = decode_jwt_token(token = access_token)
    current_time = datetime.utcnow()
    question = question.dict()
    question[CREATED_AT] = current_time
    question[UPDATED_AT] = current_time
    question[USER_ID] = decoded_access_token.get(USER_ID)
    _id = await insert_one(db = db ,collection = QUESTIONS,query = question)
    question[ID] = convert_objectId_to_string(_id.inserted_id)
    question = OutputQuestion(**question)
    return question


    

# user_id 의 question 의 질문 수정
@router.put("/question",response_model = OutputQuestion,responses = {**response_status_code})
async def update_question(question : Input_Question,question_id,request:Request,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)],access_token : str =  Header()):
    req = dict(request)
    req = convert_binary_to_string(req)
    verfiy_token(req,access_token = access_token)
    decoded_access_token = decode_jwt_token(token = access_token)
    query = {
    USER_ID : decoded_access_token.get(USER_ID),
    ID : ObjectId(question_id),
    }
    # 업데이트시간 
    modify_query = question.dict()
    modify_query[UPDATED_AT] = datetime.utcnow()
    result = await find_one_and_update(db = db,collection = QUESTIONS,find_query = query,modify_query = modify_query )
    result = dict(result)
    serialize_id(result)
    return result

# user_id 의 question 삭제
@router.delete("/question",responses = {**response_status_code})
async def delete_question(question_id,request:Request,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)],access_token : str =  Header()):
    req = dict(request)
    req = convert_binary_to_string(req)
    verfiy_token(req,access_token = access_token)
    decoded_access_token = decode_jwt_token(token = access_token)
    query = {
        USER_ID : decoded_access_token.get(USER_ID),
        ID : ObjectId(question_id),
        }
    await delete_one(db = db,collection = QUESTIONS,query = query)
    response = JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {}
                            )
    return response
 

@router.post("/answer",response_model = AnswerOutput,responses = {**response_status_code})
async def post_answer(question_id,answer : Answer,request:Request,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)],access_token : str =  Header()):
    req = dict(request)
    req = convert_binary_to_string(req)
    # Refresh 와 accessToken 발급 ID 같은지 check
    verfiy_token(req,access_token = access_token)
    decoded_access_token = decode_jwt_token(token = access_token)
    answer = answer.dict()
    set_datetime(answer)
    query = {
        USER_ID : decoded_access_token.get(USER_ID),
        ITEM_ID : ObjectId(question_id),
        CONTENT : answer,
    }
    _id = await insert_one(db = db,collection = ANSWERS,query = query)
    result = {
        USER_ID : decoded_access_token.get(USER_ID),
        ITEM_ID : question_id,
        ANSWER_ID : convert_objectId_to_string(_id.inserted_id),
        CONTENT : answer,
        
    }
    response = JSONResponse(status_code = status.HTTP_201_CREATED,
                            content =  jsonable_encoder(result)
                            )
    return result

