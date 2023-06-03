from dataclasses import dataclass
from datetime import datetime,timedelta
from typing import Union
from fastapi import *
from configs.constant import *
from configs.constant import ACCESS_TOKEN_EXPIRE_MINUTES
from jose import JWTError, jwt
from pydantic import EmailStr
@dataclass
class SessionToken:
    user_id:str
    iat : datetime
    exp : datetime
    client_ip : str
    token_type : str 


@dataclass
class EmailToken:
    email: EmailStr
    iat : datetime
    exp : datetime 
    client_ip : str
    token_type : str 

@dataclass 
class AccountToken:
    user_id : str
    client_ip: str 
    iat : datetime 
    exp : datetime 
    token_type : str 


@dataclass
class Encode_Token:
    token : str


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


def decode_jwt_token(token : str):
    decoded_jwt = jwt.decode(token,SECRETKEY,algorithms = [ALGORITHM])
    return decoded_jwt

def check_client_ip(decoded_token,request:Request):
    if decoded_token.get("client_ip") != request.client.host :
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "invalid Token !")

def check_token_type(decoded_token,token_type:str):
    if decoded_token.get("token_type") != token_type:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "invalid Token !")

def check_email(decoded_token,email):
    if decoded_token.get("email") != email:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "invalid Token !")

