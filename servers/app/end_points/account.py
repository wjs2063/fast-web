from fastapi import *
from fastapi.responses import *
from models.database import *
from schemas.userSchema import *
from schemas.token import *
router = APIRouter()


@router.post("/token",response_model = AccountToken,status_code = status.HTTP_200_OK)
async def check_password(user_id : str ,password : Password,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    password = password.password
    user_info = await db.find_one({"user_id":user_id})
    if not user_info:
        raise HTTPException(status_code = status.HTTP_)
    user_info = dict(user_info) 
    if not pwd_context.verify(password,user_info["password"]):
        HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    

@router.post("/token")
async def send_password_token():
    pass 

@router.post("/reset_password")
async def reset_password():
    pass 


