
from pydantic import BaseModel,EmailStr,Field,Required,BaseConfig
from fastapi_camelcase import CamelModel
from datetime import datetime
from typing import Union
from bson.objectid import ObjectId
from enum import Enum



class Answer(CamelModel) :
    user_id : str
    item_id : str 
    answer : str 
    created_at : datetime 
    updated_at : datetime 
    class Config(BaseConfig):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example" : {
                "user_id" : "test1",
                "item_id" : "Ab1604scx1xaxx06ffsd",
                "answer" : "정답은 O(N^2) 입니다",
                "created_at" : datetime.utcnow(),
                "updated_at" : datetime.utcnow()
            }
        }
        json_encoders = {
            ObjectId: str,
            datetime:str,
        }

