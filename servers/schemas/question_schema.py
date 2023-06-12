
from pydantic import BaseModel,EmailStr,Field,Required,BaseConfig
from fastapi_camelcase import CamelModel
from datetime import datetime
from typing import Union
from bson.objectid import ObjectId

"""
Question 객체 
아이디
제목
내용
카테고리
생성날짜
수정날짜

"""

class Question(BaseModel):
    user_id :str
    nickname : str
    subject : str
    content : str
    category : str
    answer :  Union[list,None] = None
    created_time : str = Field(...)
    updated_time : str = Field(...)
    language : str = Field(...)
    is_completed : bool
    voted : list

    class Config(BaseConfig):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example":{
                "user_id":"test_id1",
                "nickname":"test_nick",
                "subject":"DFS/BFS Base Code",
                "content":"DFS란말이죠?",
                "category":"DFS/BFS",
                "language":"Python",
                "answer": [],
                "is_completed":False,
                "voted" : [],
                "create_time":datetime.utcnow(),
                "update_time":datetime.utcnow(),
            }
        }
        json_encoders = {
            ObjectId: str,
            datetime:str,
        }