from fastapi import *
from fastapi.responses import *
from pymongo import ReturnDocument
from datetime import datetime 
from configs.constant import *

async def insert_one(db,collection,query):
    _id = await db[collection].insert_one(query)
    return _id

async def find_one(db,collection,query):
    return await db[collection].find_one(query)

async def find_many(db,collection, query):
    return await db[collection].find(query)

async def find_many_with_pagination(db,collection,query,page = 1,limit = DEFAULT_LIMIT):
    offset = (page - 1) * limit
    return await db[collection].find(query).skip(offset).limit(limit).to_list(length = DEFAULT_LIMIT)

async def count_total_documents(db,collection,query):
    return await db[collection].count_documents(query)

async def find_one_and_update(db,collection,find_query,modify_query):
    result = await db[collection].find_one_and_update(
        find_query,
        {
            "$set" : modify_query
        },
        return_document = ReturnDocument.AFTER
    )
    return result 

async def insert_login_history(db,collection,data:dict,token:str,request:Request):
    docs = {
        USER_ID:data[USER_ID],
        CLIENT_IP : request["headers"]["x-real-ip"] if request["headers"].get("x-real-ip") else request["client"][0],
        LOGIN_TIME : datetime.utcnow(),
        ACCESS_TOKEN :token,
        DEVICE : request["headers"]["user-agent"]
    }
    return await insert_one(db,collection,docs)

async def insert_logout_history(db,collection,decoded_jwt, token : str ,request :Request):
    docs = {
        USER_ID:decoded_jwt.get(USER_ID),
        CLIENT_IP : request["headers"]["x-real-ip"] if request["headers"].get("x-real-ip") else request["client"][0],
        LOGOUT_TIME : datetime.utcnow(),
        ACCESS_TOKEN : token,
        DEVICE : request["headers"]["user-agent"]
    }
    return await insert_one(db ,collection ,docs)

from typing import List
def serealize(docs : List[dict] ):
    for i,v in enumerate(docs):
        v["_id"] = str(v["_id"])
        docs[i] = v 
    return docs 