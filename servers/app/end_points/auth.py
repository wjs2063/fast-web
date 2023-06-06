from fastapi import *
from fastapi.responses import *
from fastapi.encoders import jsonable_encoder
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
from models.crud import *
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
import os
from email.mime.text import MIMEText
from smtplib import SMTP
from configs.security import *
import pymongo

router = APIRouter()

@router.post("/login",status_code = status.HTTP_200_OK)
async def login (request : Request,
                 form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                 db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)],
                 ):
    user = await get_user(db,form_data.username)
    if not user :
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "user is not exist",
                            #headers={"WWW-Authenticate": "Bearer"},
                            )
    verify_password(form_data.password,user["password"])

    # proxy 환경에서 사용하면 로직이 달라짐.
    data = {
        "user_id" : user["user_id"],
        "token_type" : "login"
    }
    refresh_token = await get_refresh_token(db,request = request,data = data,user_id = user["user_id"])
    access_token = encode_access_token(request = request,
        data = data, expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token = Encode_Token(token = access_token)
    response = JSONResponse(
    content = {
        "token":jsonable_encoder(token)
    }
    )
    response.set_cookie(key = "refresh_token",value = refresh_token,httponly = True)
    print(response.headers)
    return response



@router.post("/sign-up",response_model = UserData,status_code = status.HTTP_201_CREATED)
async def create_user(request:Request,user :User,token : Encode_Token,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    user = dict(user)
    encode_token = token.token
    current_user = await get_user(db,user["user_id"])
    if current_user :
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "이미 존재하는 회원 입니다.")
    decoded_jwt = decode_jwt_token(token = encode_token)
    #verify_client_ip(decoded_jwt,request)
    verify_email(decoded_jwt,user["email"])
    user["password"] = pwd_context.hash(user["password"])
    set_datetime(user)
    _id = await insert_one(db,user)
    return user

@router.get("/userId",status_code = status.HTTP_200_OK)
async def duplicate_userId(user_id,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    current_user = await get_user(db,user_id)
    if current_user:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "이미 존재하는 회원ID 입니다.")
    return JSONResponse(content = None)

@router.get("/email",status_code = status.HTTP_200_OK)
async def duplicate_email(request:Request,email_str : EmailStr,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    query = {"email":email_str}
    current_user = await find_one(db,query)
    if current_user:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "이미 가입한 이메일 입니다.")
    return JSONResponse(content = {"message" : "사용가능한 이메일입니다"})



@router.get("/register/validation",status_code = status.HTTP_200_OK)
async def validate_token(request:Request,token:str,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    try :
        decoded_jwt = jwt.decode(token,SECRETKEY,algorithms = [ALGORITHM])
        if decoded_jwt.get("token_type") != "email":
            HTTPException(status_code = status.HTTP_404_NOT_FOUND)
        
        query = {
            "email" :decoded_jwt.get("email")
        }
        user = await find_one(db,query)

        if user:
            HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "이미 존재하는 이메일입니다.")
        return JSONResponse(status_code = status.HTTP_200_OK, content = {"message" : "token validation Success!"})
    except Exception as e :
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,detail = str(e))

@router.post("/accessToken")
async def generate_access_token(request:Request,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb),],refresh_token: str = Header()):
    try :
        print(request)
        decoded_refresh_token = decode_jwt_token(refresh_token)
        # 만료 체크 
        if not decoded_refresh_token :
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "invalid token")
        user_id = decoded_refresh_token.get("user_id")
        data = {
        "user_id" : user_id,
        "token_type" : "login"
        }
        access_token = encode_access_token(request = request,
        data = data, expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES
        )
        token = Encode_Token(token = access_token)
        return JSONResponse(
        content = {
            "token":jsonable_encoder(token)
        }
        )
    except Exception as e :
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = str(e))