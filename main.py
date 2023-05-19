from fastapi import FastAPI,Depends
from typing import Annotated
from server.model.database import *
from pymongo import MongoClient
from server.routes.route import apps


app = FastAPI()
app.include_router(apps)



"""
@app.post("/api")
async def post(db: Annotated[MongoClient ,Depends(get_db)]):
    db.user.insert_one({"example":1})
    return "hello World!"

"""
