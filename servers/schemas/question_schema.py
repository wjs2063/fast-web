
from pydantic import BaseModel,EmailStr,Field,Required,BaseConfig
from fastapi_camelcase import CamelModel
from datetime import datetime
from typing import Union,List
from bson.objectid import ObjectId
from enum import Enum
"""
Question 객체 
아이디
제목
내용
카테고리
생성날짜
수정날짜

"""

class LanguageEnum(str,Enum):
    python = "python"
    C = "C/C++"
    Go = "Go"
    Javascript = "Javascript"
    Rust = "Rust"
    Java = "Java"
    Ruby = "Ruby"
    Kotlin = "Kotlin"
    Swift = "Swift"


    

class Input_Question(CamelModel):
    user_id :str
    nickname : str
    subject : str
    content : str
    category : str
    #created_at : str = Field(...)
    #updated_at : str = Field(...)
    language : LanguageEnum
    is_completed : bool

    class Config(BaseConfig):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example":{
                "user_id" : "aaa1234",
                "nickname":"test_nick",
                "subject":"DFS/BFS Base Code",
                "content":"DFS란말이죠?",
                "category":"DFS/BFS",
                "language":"python",
                "is_completed":False,
                #"created_time":datetime.utcnow(),
                #"updated_time":datetime.utcnow(),
            }
        }
        json_encoders = {
            ObjectId: str,
            datetime:str,
        }

class OutputQuestion(CamelModel):
    id : str =  Field (alias = "_id")
    user_id :str
    nickname : str
    subject : str
    content : str
    category : str
    created_at : datetime
    updated_at : datetime
    language : LanguageEnum
    is_completed : bool
    class Config(BaseConfig):
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId :str
        }
        schema_extra = {
            "example":{
                "_id": "ffa13a648d8da7857f30dd73c47afbd2",
                "userId": "aaa1234",
                "nickname": "test_nick",
                "subject": "DFS/BFS Base Code",
                "content": "DFS란말이죠?",
                "category": "DFS/BFS",
                "createdAt": "2023-06-17T10:40:39.550743",
                "updatedAt": "2023-06-17T10:40:39.550743",
                "language": "python",
                "isCompleted": False
                }
        }


class QuestionList(BaseModel):
    __root__ : List[OutputQuestion]