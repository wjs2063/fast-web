
from pydantic import BaseModel,EmailStr,Field,Required,BaseConfig
from fastapi_camelcase import CamelModel
from datetime import datetime
from typing import Union
from bson.objectid import ObjectId
from enum import Enum



class Comment(CamelModel):
    user_id : str 
    item_id : str 
    comment : str 
    created_at : datetime 
    class Config(BaseConfig):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example" : {
                "user_id" : "test1",
                "item_id" : "Ab1604scx1xaxx06ffsd",
                "comment" : "O(N) 아닐까요?",
                "created_at" : datetime.utcnow(),
            }
        }
        json_encoders = {
            ObjectId: str,
            datetime:str,
        }

class Details : 
    DateAdded : datetime

class Like(CamelModel):
    user_id : str 
    item_id : str 
    details : Details
    class Config(BaseConfig):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example" : {
                "user_id" : "test1",
                "item_id" : "Ab1604scx1xaxx06ffsd",
                "details" : Details(DateAdded = datetime.utcnow())
            }
        }
        json_encoders = {
            ObjectId: str,
            datetime:str,
        }
