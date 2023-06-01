from dataclasses import dataclass
from pydantic import constr
from fastapi_camelcase import CamelModel
from bson import ObjectId
from typing import *
from pydantic import BaseModel,EmailStr,Field,Required,BaseConfig
from datetime import datetime,date
from passlib.context import CryptContext
from enum import Enum
# instance
pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

class Gender(str,Enum):
    남성 : "남성"
    여성 : "여성"

class User(CamelModel):
    name : str = Field(min_length = 2,max_length = 15)
    user_id: str = Field(min_length = 2,max_length = 15)
    email : EmailStr = Field(default = None)
    password :str = Field(min_length = 7,max_length = 15)
    nickname : str = Field(min_length = 2,max_length = 15)
    gender : str
    birth_year : int = Field(ge = 1900,le = date.today().year)
    birth_month : int = Field(ge = 1,le = 12)
    birth_day : int = Field(ge = 1, le = 31)
    disabled : bool

    class Config:
        use_enum_values = True
        schema_extra = {
            "example":{
                "name":"jaehyeon",
                "user_id":"aaa1234",
                "email":"kkk@naver.com",
                "gender" :"남성",
                "password":"1234567",
                "nickname":"user1",
                "birth_year" :1900,
                "birth_month" :5,
                "birth_day" : 25,
                "disabled":True,
            }
        }



class UserData(CamelModel):
    #id : str = Field(...,alias = "_id")
    name : str = Field(min_length = 2,max_length = 15)
    user_id: str = Field(min_length = 2,max_length = 15)
    email : EmailStr = Field(default = None)
    nickname : str = Field(min_length = 2,max_length = 15)
    disabled : Union[bool,None]
    class Config(BaseConfig):
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId : str
        }

class Password(CamelModel):
    password : str 


# function

def serialize_id(data):
    data["_id"] = str(data["_id"])


def set_datetime(data):
    data["create_time"] = datetime.utcnow()
    data["update_time"] = datetime.utcnow()

async def get_user(db,user_id):
    data = await db.users.find_one({"user_id":user_id})
    if not data :
        return None
    return  dict(data)