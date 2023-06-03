from fastapi import *
from fastapi.responses import *
from models.database import *
from models.crud import *
from schemas.userSchema import *
from schemas.token import *
router = APIRouter()


@router.post("/token",status_code = status.HTTP_200_OK)
async def account_token(request : Request,user_id : str ,password : Password,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    password = password.password
    query = {"user_id":user_id}
    user_info = await find_one(db,query)
    if not user_info:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    user_info = dict(user_info) 
    if not pwd_context.verify(password,user_info["password"]):
        HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    data = {
        "user_id" : user_id,
        "token_type" : "account",
        "client_ip" : request.client.host
    }
    account_token = create_access_token(data = data)
    return account_token


@router.post("/reset_password")
async def reset_password():
    pass 


