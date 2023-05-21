from fastapi import *
from fastapi.responses import *
from typing import Annotated
from models.database import *
from fastapi.staticfiles import StaticFiles
from configs.constant import *
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime,timedelta
from schemas.userSchema import *
from bson import ObjectId
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
apps = APIRouter()

@apps.get("/")
async def main():
    return "hello"
#apps.mount("/templates",StaticFiles(directory = "static",html = True),name = "static")
@apps.post("/api")
async def test(db: Annotated[MongoClient ,Depends(get_db)]):
    db.user.insert_one({"example":datetime.utcnow()})
    return "hello World!"

"""
@apps.post("/api/user",response_model = UserData,status_code = 201)
async def create_user(user :User,db: Annotated[MongoClient ,Depends(get_db)]):
    user = dict(user)
    # 중복체크
    db.users.insert_one(user)
    data = dict(db.users.find_one(user))
    # serialize
    #data["_id"] = str(data["_id"])
    return data
"""

@apps.post("/api/user",response_model = UserData,status_code = 201)
async def create_user_async(user :User,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    user = dict(user)
    set_datetime(user)
    await db.users.insert_one(user)
    data = dict(await db.users.find_one(user))
    #serializeId(data)
    return data
