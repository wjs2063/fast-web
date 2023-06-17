
from pydantic import BaseModel,EmailStr,Field,Required,BaseConfig
from fastapi_camelcase import CamelModel
from datetime import datetime
from typing import Union
from bson.objectid import ObjectId
from enum import Enum



class Answer(CamelModel) :
    answer : str 
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

