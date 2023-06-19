
from pydantic import BaseModel,EmailStr,Field,Required,BaseConfig
from fastapi_camelcase import CamelModel
from datetime import datetime
from typing import Union
from bson.objectid import ObjectId
from configs.constant import *
from enum import Enum



class Answer(CamelModel) :
    answer : str = Field(min_length = 5,max_length = 5000)
    class Config(BaseConfig):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example" : {
                "answer" : "정답은 O(N^2) 입니다",
            }
        }
        json_encoders = {
            ObjectId: str,
            datetime:str,
        }

class AnswerOutput(CamelModel):
    user_id : str = Field(min_length = 2,max_length = 15)
    item_id : str = Field(min_length = 2,max_length = 200)
    answer_id : str 
    content : dict 
    class Config(BaseConfig):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example" : {
                USER_ID : "aaa1234",
                ITEM_ID : "64884bc2cbdfc78b6279adsasd6f5",
                ANSWER_ID : "ffd648add86b122cd8ed98fa5b566",
                CONTENT : {
                    "answer": "정답은 O(N^2) 입니다",
                    "create_time": "2023-06-17T10:10:57.752090",
                    "update_time": "2023-06-17T10:10:57.752091"
                }
            }
        }
        json_encoders = {
            ObjectId: str,
            datetime:str,
        }