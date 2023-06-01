from fastapi import stauts
from fastapi.responses import *

async def insert_one(db,query):
    _id = await db.insert_one(query)
    return _id

async def find_one(db,query):
    result = await db.find_one(query)
    pass
