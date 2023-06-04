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
pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    current_time = datetime.utcnow()
    if expires_delta:
        expire_time = current_time + timedelta(minutes = int(ACCESS_TOKEN_EXPIRE_MINUTES))
    else:
        expire_time = current_time + timedelta(minutes = 15)
    to_encode.update({"iat": current_time})
    to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(to_encode, SECRETKEY, algorithm =  ALGORITHM)
    return encoded_jwt

def encode_jwt_token(data):
    return jwt.encode(data, SECRETKEY, algorithm =  ALGORITHM)

def decode_jwt_token(token : str):
    decoded_jwt = jwt.decode(token,SECRETKEY,algorithms = [ALGORITHM])
    return decoded_jwt

def verify_client_ip(decoded_token,request:Request):
    if decoded_token.get("client_ip") != request.client.host :
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "invalid Token !")

def verify_token_type(decoded_token,token_type:str):
    if decoded_token.get("token_type") != token_type:
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
