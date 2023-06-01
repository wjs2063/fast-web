from fastapi import *
from fastapi.responses import *
from typing import Annotated
from models.database import *
from schemas.token import *
from fastapi.staticfiles import StaticFiles
from configs.constant import *
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime,timedelta
from schemas.userSchema import *
from bson import ObjectId


router = APIRouter()

@router.post("/database/reset",status_code = status.HTTP_200_OK)
async def database_reset(password:Password,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    password = password.password 
    if password != "admin123":
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    await db.users.drop()
    return 


