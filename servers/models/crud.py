from fastapi import *
from fastapi.responses import *
from pymongo import ReturnDocument

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