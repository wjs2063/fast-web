from dataclasses import dataclass
from pydantic import constr
from fastapi_camelcase import CamelModel
from bson import ObjectId
from typing import *
from pydantic import BaseModel,EmailStr,Field,Required,BaseConfig

class User(CamelModel):
    name : str = Field(min_length = 2,max_length = 15)
    user_id: str = Field(min_length = 2,max_length = 15)
    email : EmailStr = Field(default = None)
    password :str = Field(min_length = 7,max_length = 15)
    nickname : str = Field(min_length = 2,max_length = 15)
    disabled : bool

    class Config:
        schema_extra = {
            "example":{
                "name":"jaehyeon",
                "user_id":"aaa1234",
                "email":"kkk@naver.com",
                "password":"1234567",
                "nickname":"user1",
                "disabled":"False",
            }
        }
class UserData(BaseModel):
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
            ObjectId: str
        }
