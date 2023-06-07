from fastapi import *
from fastapi.responses import *
from models.database import *
from models.crud import *
from schemas.userSchema import *
from schemas.token import *
from configs.security import *

router = APIRouter()


@router.post("/token",status_code = status.HTTP_200_OK)
async def account_token(request : Request,user_id : str ,password : Password,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    request = convert_binary_to_string(request)
    password = password.password
    query = {"user_id":user_id}
    user_info = await find_one(db,query)
    if not user_info:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    user_info = dict(user_info) 
    verify_password(password,user_info["password"])
    data = {
        "user_id" : user_id,
        "token_type" : "account",
    }
    account_token = encode_access_token(request = request,data = data)
    return account_token


@router.post("/reset_password",status_code = status.HTTP_200_OK)
async def reset_password(request:Request,token : str,password : Password,
                         db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    request = convert_binary_to_string(request)
    decoded_token = decode_jwt_token(token)
    query = {
        "user_id":decoded_token.get("user_id")
        }
    user = await find_one(db,query)
    #verify_client_ip(decoded_token = decoded_token,request = request)
    verify_token_type(decoded_token = decoded_token,token_type = "account")
    password = password.password 
    find_query = {
        "user_id" : decoded_token.get("user_id")
    }
    modify_query = {
        "password" : pwd_context.hash(password)
    }
    result = await find_one_and_update(db,find_query,modify_query)
    return 




