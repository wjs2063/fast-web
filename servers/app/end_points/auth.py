from fastapi import *
from fastapi.responses import *
from fastapi.encoders import jsonable_encoder
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
from models.crud import *
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
import os
from email.mime.text import MIMEText
from smtplib import SMTP
from configs.security import *
import pymongo
from http.cookies import SimpleCookie
from configs.status_code import *
router = APIRouter()

@router.post("/login",response_model = LoginOutput,status_code = status.HTTP_200_OK,responses = {**response_status_code})
async def login (request : Request,
                 form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                 db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)],
                 ):
    request = convert_binary_to_string(request)
    user = await get_user(db,form_data.username)
    if not user :
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "user is not exist",
                            #headers={"WWW-Authenticate": "Bearer"},
                            )
    verify_password(form_data.password,user[PASSWORD])

    # proxy 환경에서 사용하면 로직이 달라짐.
    data = {
        USER_ID : user[USER_ID],
        NICKNAME : user[NICKNAME],
        USAGE : LOGIN
    }
    refresh_token = await get_refresh_token(db,request = request,data = data)
    access_token = encode_access_token(request = request,
        data = data, expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token = Encode_Token(token = access_token)

    response = JSONResponse(
    content = {
        NICKNAME : user[NICKNAME],
        TOKEN:jsonable_encoder(token)
    }
    )
    response.set_cookie(key = REFRESH_TOKEN,value = refresh_token,httponly = True,expires = 1200,max_age = 1200,samesite = "none",secure = True)
    await insert_login_history(db = db ,collection = LOGIN,data = data , token = access_token,request = request)
    return response

@router.post("/logout",status_code = status.HTTP_200_OK,responses = {**response_status_code})
async def logout(request:Request,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)],access_token : str =  Header(),):
    request = convert_binary_to_string(request)
    cookies = parse_cookie(request)
    # refresh token 있는지 check
    if not cookies.get(REFRESH_TOKEN):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "Invalid Token"
            )
    # access_token 
    if not access_token :
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                    detail = "Invalid Token"
        )
    # JWT_TOKEN 자동으로 raise error
    decoded_jwt = decode_jwt_token(token = access_token)
    response = JSONResponse(content = None)
    response.set_cookie(key = REFRESH_TOKEN,value = None,httponly = True,expires = 1200,max_age = 1200,samesite = "none",secure = True)
    await insert_logout_history(db = db,collection = "logout",decoded_jwt = decoded_jwt,token = access_token,request = request)
    # access token 유효한지 check
    return response


@router.post("/sign-up",response_model = UserData,status_code = status.HTTP_201_CREATED,responses = {**response_status_code})
async def create_user(request:Request,user :User,token : Encode_Token,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    request = convert_binary_to_string(request)
    user = dict(user)
    encode_token = token.token
    current_user = await get_user(db,{USER_ID:user[USER_ID]})
    if current_user :
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "이미 존재하는 아이디 입니다.")
    if await find_one(db = db,collection = USERS,query = {EMAIL:user[EMAIL]}):
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "이미 존재하는 이메일 입니다.")
    if await find_one(db = db,collection = USERS,query = {NICKNAME:user[NICKNAME]}):
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "이미 존재하는 닉네임 입니다.")
    decoded_jwt = decode_jwt_token(token = encode_token)
    #verify_client_ip(decoded_jwt,request)
    verify_email(decoded_jwt,user[EMAIL])
    user[PASSWORD] = pwd_context.hash(user[PASSWORD])
    set_datetime(user)
    _id = await insert_one(db,collection = USERS,query = user)
    return user

@router.get("/userId",status_code = status.HTTP_200_OK,responses = {**response_status_code})
async def duplicate_userId(user_id,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    current_user = await get_user(db,user_id)
    if current_user:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "이미 존재하는 회원ID 입니다.")
    return 

@router.get("/email",responses = {**response_status_code})
async def duplicate_email(request:Request,email_str : EmailStr,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    query = {EMAIL:email_str}
    current_user = await find_one(db = db,collection = USERS,query = query)
    if current_user:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "이미 가입한 이메일 입니다.")
    return JSONResponse(content = {"message" : "사용가능한 이메일입니다"})



@router.get("/register/validation",responses = {**response_status_code})
async def validate_token(request:Request,token:str,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    decoded_jwt = jwt.decode(token,SECRETKEY,algorithms = [ALGORITHM])
    if decoded_jwt.get(USAGE) != EMAIL:
        HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    
    query = {
        EMAIL :decoded_jwt.get(EMAIL)
    }
    user = await find_one(db = db,collection = USERS,query = query)

    if user:
        HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "이미 존재하는 이메일입니다.")
    return JSONResponse(status_code = status.HTTP_200_OK, content = {"message" : "token validation Success!"})

@router.post("/accessToken",responses = {**response_status_code})
async def generate_access_token(request:Request,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb),]):
    request = convert_binary_to_string(request)
    cookies = parse_cookie(request)
    refresh_token = cookies.get(REFRESH_TOKEN)
    if not refresh_token or refresh_token == "None":
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Login Required")
    decoded_refresh_token = decode_jwt_token(refresh_token)

    # 만료 체크 
    if not decoded_refresh_token :
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "invalid token")
    user_id = decoded_refresh_token.get(USER_ID)
    data = {
    USER_ID : user_id,
    USAGE : LOGIN
    }
    access_token = encode_access_token(request = request,
    data = data, expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token = Encode_Token(token = access_token)
    return JSONResponse(
    content = {
        TOKEN:jsonable_encoder(token)
    }
    )