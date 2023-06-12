from fastapi import *
from fastapi.responses import *
from pymongo import ReturnDocument
from datetime import datetime 
from configs.constant import *
async def insert_one(db,query):
    _id = await db.users.insert_one(query)
    return _id

async def find_one(db,query):
    result = await db.users.find_one(query)
    return result 

async def find_one_and_update(db,find_query,modify_query):
    result = await db.users.find_one_and_update(
        find_query,
        {
            "$set" : modify_query
        },
        return_document = ReturnDocument.AFTER
    )
    return result 

async def insert_login_history(db,data:dict,token:str,request:Request):
    docs = {
        USER_ID:data[USER_ID],
        CLIENT_IP : request["headers"]["x-real-ip"] if request["headers"].get("x-real-ip") else request["client"][0],
        LOGIN_TIME : datetime.utcnow(),
        ACCESS_TOKEN :token,
        DEVICE : request["headers"]["user-agent"]
    }
    return await db.login.insert_one(docs)

async def insert_logout_history(db,decoded_jwt, token : str ,request :Request):
    docs = {
        USER_ID:decoded_jwt.get(USER_ID),
        CLIENT_IP : request["headers"]["x-real-ip"] if request["headers"].get("x-real-ip") else request["client"][0],
        LOGOUT_TIME : datetime.utcnow(),
        ACCESS_TOKEN : token,
        DEVICE : request["headers"]["user-agent"]
    }
    return await db.logout.insert_one(docs)