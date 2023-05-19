from pymongo import MongoClient
from ..config.constant import *
from pymongo.errors import ConnectionFailure



async def get_db():
    db = MongoClient(ORIGIN_MONGODB)
    try:
        yield db.local
    finally:
        db.close()
