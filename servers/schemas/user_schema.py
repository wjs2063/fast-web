from dataclasses import dataclass
from pydantic import constr
from fastapi_camelcase import CamelModel
from fastapi import *
from bson import ObjectId
from typing import *
from pydantic import BaseModel,EmailStr,Field,Required,BaseConfig,ValidationError, validator
from datetime import datetime,date
from passlib.context import CryptContext
from configs.constant import *
from enum import Enum
# instance

class GenderEnum(str,Enum):
    남자 = "남자"
    여자 = "여자"

class User(CamelModel):
    name : str = Field(min_length = 2,max_length = 15)
    user_id: str = Field(min_length = 2,max_length = 15)
    email : EmailStr = Field(default = None)
    password :str = Field(min_length = 5,max_length = 64)
    nickname : str = Field(min_length = 2,max_length = 15)
    gender : GenderEnum
    birth_year : int = Field(ge = 1900,le = date.today().year)
    birth_month : int = Field(ge = 1,le = 12)
    birth_day : int = Field(ge = 1, le = 31)
    disabled : bool
    @validator('name')
    def name_validator(cls,v):
        return v 
    @validator('user_id')
    def userId_validator(cls,v):
        return v 
    @validator('email')
    def email_validator(cls,v):
        return v 
    @validator('nickname')
    def nickname_validator(cls,v):
        return v 
    @validator('password')
    def password_validator(cls,v):
        return v 

    class Config:
        use_enum_values = True
        schema_extra = {
            "example":{
                "name":"jaehyeon",
                "user_id":"aaa1234",
                "email":"kkk@naver.com",
                "gender" :"남자",
                "password":"1234567",
                "nickname":"user1",
                "birth_year" :1900,
                "birth_month" :5,
                "birth_day" : 25,
                "disabled" : True
            }
        }



class UserData(CamelModel):
    #id : str = Field(...,alias = "_id")
    name : str = Field(min_length = 2,max_length = 15)
    user_id: str = Field(min_length = 2,max_length = 15)
    email : EmailStr = Field(default = None)
    nickname : str = Field(min_length = 2,max_length = 15)
    disabled : Union[bool,None]

    @validator('name')
    def name_validator(cls,v):
        return v 
    @validator('user_id')
    def userId_validator(cls,v):
        return v  
    @validator('email')
    def email_validator(cls,v):
        return v 
    @validator('nickname')
    def nickname_validator(cls,v):
        return v 

    class Config(BaseConfig):
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId : str
        }
        schema_extra = {
            "example" : {
                "name" : "전재현",
                "user_id" : "aaa1234",
                "email" : "kkk@example.com",
                "nickname" : "test_user",
                "disabled" : False,
            }
        }


class LoginOutput(CamelModel):
    nickname : str 
    token : dict 
    class Config(BaseConfig):
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId : str
        }
        schema_extra = {
            "example" : {
                NICKNAME : "test_user1",
                TOKEN :{TOKEN: "eyJhbGcdfOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWFhMTIzNCIsasdvclIjoibG9naW4iLCJpYXQiOjE2ODY5OTM3MjgsImV4cCI6MTY4Njk5NTUyOCwiY2xpZW50X2lwIjoiNTkdda5jQzLjE2NiJ9.lG1knoN8BsXQrlUwdf5wI5BOQMhvFQ9ddh-Myd2TEJ0"}
            }
        }
    

class Password(CamelModel):
    password : str = Field(min_length = 5,max_length = 64)


# function

def serialize_id(data):
    data[ID] = str(data[ID])


def set_datetime(data):
    data[CREATED_AT] = datetime.utcnow()
    data[UPDATED_AT] = datetime.utcnow()

async def get_user(db,query):
    data = await db.users.find_one(query)
    if not data :
        return None
    return  dict(data)

def verify_password(plain_password,hashed_password):
    if not pwd_context.verify(plain_password,hashed_password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "Invalid password",
                            #headers={"WWW-Authenticate": "Bearer"},
                            )

