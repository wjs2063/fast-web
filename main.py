from fastapi import FastAPI,Depends
from typing import Annotated
from server.model.database import *
from pymongo import MongoClient


app = FastAPI()



@app.post("/api")
async def post(db: Annotated[MongoClient ,Depends(get_db)]):
    db.user.insert_one({"example":1})
    return "hello World!"
