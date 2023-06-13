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




