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

router = APIRouter()

@router.post("/login",response_model = Token,status_code = status.HTTP_200_OK)
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
    if not pwd_context.verify(form_data.password,user['password']):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "Invalid password",
                            #headers={"WWW-Authenticate": "Bearer"},
                            )
    # proxy 환경에서 사용하면 로직이 달라짐.
    data = {
        "user_id" : user["user_id"],
        "ip_addr" : request.client.host
    }

    access_token = create_access_token(
        data = data, expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES
    )

    content = {"message" : "fastapi"}
    headers = {"access_token":access_token,"token_type": "bearer"}
    return JSONResponse(content = content,headers = headers)



@router.post("/sign-up",response_model = UserData,status_code = status.HTTP_201_CREATED)
async def create_user(user :User,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)],token = Header()):
    user = dict(user)
    current_user = await get_user(db,user["user_id"])
    if current_user :
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "이미 존재하는 회원 입니다.")
    decoded_jwt = jwt.decode(token,SECRETKEY,algorithms = [ALGORITHM])
    if decoded_jwt.get("user_id") != user["user_id"]:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail = "invalid Token")
    if decoded_jwt.get("email") != user["email"]:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "invalid Token")

    user["password"] = pwd_context.hash(user["password"])
    set_datetime(user)
    await db.users.insert_one(user)
    return user

@router.post("/userId",status_code = status.HTTP_200_OK)
async def duplicate_userId(user_id,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    current_user = await get_user(db,user_id)
    if current_user:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "이미 존재하는 회원ID 입니다.")
    return JSONResponse(content = None)

@router.post("/email",status_code = status.HTTP_200_OK)
async def duplicate_email(email_str : EmailStr,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    current_user = await db.users.find_one({"email":email_str})
    if current_user:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "이미 가입한 이메일 입니다.")
    return JSONResponse(content = {"message" : "사용가능한 이메일입니다"})



@router.post("/register/validation",status_code = status.HTTP_200_OK)
async def validate_token(token:str,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    decoded_jwt = jwt.decode(token,SECRETKEY,algorithms = [ALGORITHM])
    user_id = decoded_jwt.get("user_id")
    email = decoded_jwt.get("email")
    query = {
        "user_id":user_id,
        "email" : email
    }
    user = await db.users.find_one(query)
    if user:
        HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "이미 존재하는 이메일입니다.")
    return JSONResponse(status_code = status.HTTP_200_OK, content = {"message" : "token validation Success!"})

