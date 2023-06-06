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
pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def encode_access_token(request:Request,data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    current_time = datetime.utcnow()
    if expires_delta:
        expire_time = current_time + timedelta(minutes = int(expires_delta))
    else:
        expire_time = current_time + timedelta(minutes = 15)
    r = dict(request)
    to_encode.update({"iat": current_time})
    to_encode.update({"exp": expire_time})
    to_encode.update({"client_ip":r["headers"][0][1].decode()})
    print(to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRETKEY, algorithm =  ALGORITHM)
    return encoded_jwt

def encode_refresh_token(request:Request,data:dict):
    to_encode = data.copy()
    current_time = datetime.utcnow()
    expire_time = current_time + timedelta(days = int(REFRESH_TOKEN_EXPIRE_DAY))
    r = dict(request)
    to_encode.update({"iat": current_time})
    to_encode.update({"exp": expire_time})
    to_encode.update({"client_ip":r["headers"][0][1].decode()})
    print(to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRETKEY, algorithm =  ALGORITHM)
    return encoded_jwt

async def get_refresh_token(db,request,data:dict,user_id):
    refresh_token = await db.token.find({"user_id": user_id}).sort([("created_at",pymongo.DESCENDING)]).limit(1).to_list(length = 1)
    if not refresh_token:
        query  = {
            "user_id": user_id,
            "refresh_token" : encode_refresh_token(request = request,data = data),
            "created_at":datetime.utcnow()
            }
        await db.token.insert_one(query)
        refresh_token = [query]
    refresh_token = refresh_token[0]["refresh_token"]
    return refresh_token

def encode_jwt_token(data):
    return jwt.encode(data, SECRETKEY, algorithm =  ALGORITHM)

def decode_jwt_token(token : str):
    decoded_jwt = jwt.decode(token,SECRETKEY,algorithms = [ALGORITHM])
    if decoded_jwt["exp"] < time.time():
        return None
    return decoded_jwt

def verify_client_ip(decoded_token,request:Request):
    if decoded_token.get("client_ip") != request.client.host :
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "invalid Token !")

def verify_token_type(decoded_token,token_type:str):
    if decoded_token.get("token_type") != token_type:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "invalid Token !")


def verify_user_id(decoded_token,user_id):
    if decoded_token.get("user_id") != user_id:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "invalid Token !")


def verify_email(decoded_token,email):
    if decoded_token.get("email") != email:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "invalid Token !")
    

async def get_user(db,user_id):
    query = {
        "user_id" : user_id
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
