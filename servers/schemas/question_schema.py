
from pydantic import BaseModel,EmailStr,Field,Required,BaseConfig
from fastapi_camelcase import CamelModel
from datetime import datetime
from typing import Union,List
from bson.objectid import ObjectId
from enum import Enum
from configs.constant import *
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
    subject : str
    content : str
    category : CategoryEnum
    #created_at : str = Field(...)
    #updated_at : str = Field(...)
    language : LanguageEnum

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

class QuestionList(CamelModel):
    TOTAL_DOCS: int
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
                "category": "DFS/BFS",
                "createdAt": "2023-06-17T10:40:39.550743",
                "updatedAt": "2023-06-17T10:40:39.550743",
                "language": "python",
                "isCompleted": False
                }]
        }
    }
"""
class QuestionList(BaseModel):
    __root__ : List[OutputQuestion]
"""

class QuestionWithAnswer(CamelModel):
    question : dict 
    answers : List
