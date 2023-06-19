
from pydantic import BaseModel,EmailStr,Field,Required,BaseConfig,ValidationError, validator
from fastapi_camelcase import CamelModel
from datetime import datetime
from typing import Union,List
from bson.objectid import ObjectId
from enum import Enum
from configs.constant import *
from schemas.answer_schema import *
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
    Python = "Python"
    C = "C/C++"
    Go = "Go"
    Javascript = "Javascript"
    Rust = "Rust"
    Java = "Java"
    Ruby = "Ruby"
    Kotlin = "Kotlin"
    Swift = "Swift"

class CategoryEnum(str,Enum):
    dfs = "DFS"
    bfs = "BFS"
    DynamicProgramming = "DynamicProgramming"
    Implementation = "Implementation"
    BinarySearch = "BinarySearch"
    Simulation = "Simulation"
    UnionFind = "UnionFind"
    Dijkstra = "Dijkstra"
    PrefixSum = "PrefixSum"
    Sorting = "Sorting"
    Greedy = "Greedy"
    Tree = "Tree"
    Stack = "Stack"
    SlidingWindow = "SlidingWindow"
    Recursion = "Recursion"
    TopologicalSort = "TopologicalSort"
    Math = "Math"
    TwoPointer = "TwoPointer"
    String = "String"
    Graph = "Graph"
    Heap = "Heap"
    BackTracking = "BackTracking"
    Queue = "Queue"
    SegmentTree="SegmentTree"
    Hash = "Hash"
    Memozation = "Memozation"





    

class Input_Question(CamelModel):
    subject : str = Field(min_length = 5,max_length = 50)
    content : str = Field(min_length = 5,max_length = 5000)
    category : CategoryEnum
    #created_at : str = Field(...)
    #updated_at : str = Field(...)
    language : LanguageEnum

    @validator('subject')
    def subject_validator(cls,v):
        return v 
    @validator('content')
    def content_validator(cls,v):
        return v 


    class Config(BaseConfig):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example":{
                "subject":"DFS/BFS Base Code",
                "content":"DFS란말이죠?",
                "category":"DFS",
                "language":"Python",
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
    user_id : str = Field(min_length = 2,max_length = 15)
    nickname : str = Field(min_length = 2,max_length = 15)
    subject : str = Field(min_length = 5,max_length = 50)
    content : str = Field(min_length = 5,max_length = 5000)
    category : CategoryEnum
    created_at : datetime
    updated_at : datetime
    language : LanguageEnum
    is_completed : bool
    @validator('user_id')
    def userId_validator(cls,v):
        return v 
    @validator('nickname')
    def nickname_validator(cls,v):
        return v 
    @validator('subject')
    def subject_validator(cls,v):
        return v 
    @validator('content')
    def content_validator(cls,v):
        return v 

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
                "category": "DFS",
                "createdAt": "2023-06-17T10:40:39.550743",
                "updatedAt": "2023-06-17T10:40:39.550743",
                "language": "Python",
                "isCompleted": False
                }
        }

class QuestionList(CamelModel):
    TOTAL_DOCS: int = Field(ge = 0)
    QUESTIONS : List[OutputQuestion]


    class Config(BaseConfig):
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId :str
        }
        schema_extra = {
            "example":{
                TOTAL_DOCS : 1,
                QUESTIONS:[{
                "_id": "ffa13a648d8da7857f30dd73c47afbd2",
                "userId": "aaa1234",
                "nickname": "test_nick",
                "subject": "DFS/BFS Base Code",
                "content": "DFS란말이죠?",
                "category": "DFS",
                "createdAt": "2023-06-17T10:40:39.550743",
                "updatedAt": "2023-06-17T10:40:39.550743",
                "language": "Python",
                "isCompleted": False
                }]
        }
    }
        


class PageQuestionList(CamelModel):
    TOTAL_DOCS: int
    PAGE : int = Field(ge = 1)
    QUESTIONS : List[OutputQuestion]



    class Config(BaseConfig):
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId :str
        }
        schema_extra = {
            "example":{
                TOTAL_DOCS : 500,
                PAGE : 1,
                QUESTIONS:[{
                "_id": "ffa13a648d8da7857f30dd73c47afbd2",
                "userId": "aaa1234",
                "nickname": "test_nick",
                "subject": "DFS/BFS Base Code",
                "content": "DFS란말이죠?",
                "category": "DFS",
                "createdAt": "2023-06-17T10:40:39.550743",
                "updatedAt": "2023-06-17T10:40:39.550743",
                "language": "Python",
                "isCompleted": False
                } for _ in range(10)]
        }
    }
"""
class QuestionList(BaseModel):
    __root__ : List[OutputQuestion]
"""

class QuestionWithAnswer(CamelModel):
    question : OutputQuestion
    answers : List[AnswerOutput]
    class Config(BaseConfig):
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId :str
        }
        schema_extra = {
            "example":{
                QUESTION : 
                    {
                    "_id": "ffa13a648d8da7857f30dd73c47afbd2",
                    "userId": "aaa1234",
                    "nickname": "test_nick",
                    "subject": "DFS/BFS Base Code",
                    "content": "DFS란말이죠?",
                    "category": "DFS",
                    "createdAt": "2023-06-17T10:40:39.550743",
                    "updatedAt": "2023-06-17T10:40:39.550743",
                    "language": "Python",
                    "isCompleted": False
                    },
                ANSWERS:[{
                    USER_ID : "aaa1234",
                    ITEM_ID : "ffa13a648d8da7857f30dd73c47afbd2",
                    ANSWER_ID : "ffd648add86b122cd8ed98fa5b566",
                    CONTENT : {
                        "answer": "정답은 O(N^2) 입니다",
                        "create_time": "2023-06-17T10:10:57.752090",
                        "update_time": "2023-06-17T10:10:57.752091"
                    }
                }for _ in range(3)]
            }
        }


