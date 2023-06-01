from dataclasses import dataclass
from datetime import datetime,timedelta
from typing import Union
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
    iat : datetime 
    exp : datetime 
    token_type : str 



def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    current_time = datetime.utcnow()
    if expires_delta:
        expire_time = current_time + timedelta(minutes = int(ACCESS_TOKEN_EXPIRE_MINUTES))
    else:
        expire_time = current_time + timedelta(minutes = 15)
    to_encode.update({"iat": current_time})
    to_encode.update({"exp": expire_time})
    # jwt 토큰생
    encoded_jwt = jwt.encode(to_encode, SECRETKEY, algorithm =  ALGORITHM)
    # decoding
    #print(jwt.decode(encoded_jwt,SECRET_KEY,algorithms = [ALGORITHM]))
    # 생성직후 decode 잘됨
    #print(type(encoded_jwt),encoded_jwt)
    return encoded_jwt


@dataclass
class Encode_token:
    token : str