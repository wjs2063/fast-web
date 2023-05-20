from pymongo import MongoClient
from configs.constant import *


async def get_db():
    db = MongoClient(ORIGIN_MONGODB)
    try:
        yield db.local
    finally:
        db.close()
