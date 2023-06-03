from fastapi import *
from fastapi.responses import *

async def insert_one(db,query):
    _id = await db.users.insert_one(query)
    return _id

async def find_one(db,query):
    result = await db.users.find_one(query)
    return result 
