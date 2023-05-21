from pymongo import MongoClient
from configs.constant import *
from motor import motor_asyncio


async def get_db():
    db = MongoClient(LOCAL_MONGODB)
    try:
        yield db.local
    finally:
        db.close()

async def asyncdb():
    db = motor_asyncio.AsyncIOMotorClient(LOCAL_MONGODB)
    try :
        yield db["local"]
    finally :
        db.close()
