from dataclasses import dataclass
from datetime import datetime,timedelta,date
from fastapi import *
from configs.constant import *
from jose import JWTError, jwt
from fastapi_camelcase import CamelModel
from bson import ObjectId
from typing import *
from pydantic import BaseModel,EmailStr,Field,Required,BaseConfig,constr
from passlib.context import CryptContext
from models.crud import *
import pymongo
import time
from http.cookies import SimpleCookie
pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def encode_access_token(request:Request,data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    current_time = datetime.utcnow()
    if expires_delta:
        expire_time = current_time + timedelta(minutes = int(expires_delta))
    else:
        expire_time = current_time + timedelta(minutes = 15)
    to_encode.update({"iat": current_time})
    to_encode.update({"exp": expire_time})
    to_encode.update({CLIENT_IP:request["headers"]["x-real-ip"] if request["headers"].get("x-real-ip") else request["client"][0]})
    encoded_jwt = jwt.encode(to_encode, SECRETKEY, algorithm =  ALGORITHM)
    return encoded_jwt

def encode_refresh_token(request:Request,data:dict):
    to_encode = data.copy()
    current_time = datetime.utcnow()
    expire_time = current_time + timedelta(days = int(REFRESH_TOKEN_EXPIRE_DAY))
    to_encode.update({"iat": current_time})
    to_encode.update({"exp": expire_time})
    to_encode.update({CLIENT_IP:request["headers"]["x-real-ip"] if request["headers"].get("x-real-ip") else request["client"][0]})
    encoded_jwt = jwt.encode(to_encode, SECRETKEY, algorithm =  ALGORITHM)
    return encoded_jwt

async def get_refresh_token(db,request : Request,data:dict):
    # 최근에 발급받은 refresh_token 을 발급받는다
    docs = await db.token.find({USER_ID: data[USER_ID]}).sort([(CREATED_AT,pymongo.DESCENDING)]).limit(1).to_list(length = 1)
    # 최근에 발급받은 refresh_token 이 expire 됐으면 ?
    # 없거나 만료됐으면 만들자
    if not docs or datetime.utcnow() - docs[0][CREATED_AT] > timedelta(days = int(REFRESH_TOKEN_EXPIRE_DAY)):
        query  = {
            USER_ID: data[USER_ID],
            CREATED_AT:datetime.utcnow(),
            REFRESH_TOKEN : encode_refresh_token(request = request,data = data)
            }
        await db.token.insert_one(query)
        docs = [query]
    doc = docs[0]
    return doc[REFRESH_TOKEN]

def encode_jwt_token(data):
    return jwt.encode(data, SECRETKEY, algorithm =  ALGORITHM)

def decode_jwt_token(token : str):
    try :
        decoded_jwt = jwt.decode(token,SECRETKEY,algorithms = [ALGORITHM])
        return decoded_jwt
    
    except jwt.ExpiredSignature:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,deatil = "Invalid Token")
    
    except Exception as e :
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,detail = str(e))

async def get_by_email(db,email):
    return await db.user.find_one({EMAIL:email})

def verify_client_ip(decoded_token,request:Request):
    if decoded_token.get(CLIENT_IP) != request.client.host :
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "Invalid Token !")

def verify_usage(decoded_token,usage:str):
    if decoded_token.get(USAGE) != usage:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "Invalid Token !")


def verify_user_id(decoded_token,user_id):
    if decoded_token.get(USER_ID) != user_id:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "Invalid Token !")


def verify_email(decoded_token,email):
    if decoded_token.get(EMAIL) != email:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Invalid Token !")
    

async def get_user(db,user_id):
    query = {
        USER_ID : user_id
    }
    data = await find_one(db,query)
    if not data :
        return None
    return  dict(data)

def verify_password(plain_password,hashed_password):
    if not pwd_context.verify(plain_password,hashed_password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "Invalid password"
                            )

def convert_binary_to_string(request:Request):
    req = dict(request)
    req["headers"] = list(map(lambda x:list(x),req["headers"]))
    req["headers"] = dict(map(lambda x: list(map(lambda y:y.decode(),x)),req["headers"]))
    return req 

def parse_cookie(request):
    if not request["headers"].get("cookie"):
        return dict()
    cookie = SimpleCookie()
    cookie.load(request["headers"]["cookie"])
    cookies = {key: value.value  for key, value in cookie.items()}
    return cookies 



