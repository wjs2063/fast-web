from fastapi import *
from fastapi.responses import *
from models.database import *
from models.crud import *
from schemas.user_schema import *
from schemas.token_schema import *
from configs.security import *
from configs.status_code import *
from configs.constant import *
router = APIRouter()


@router.post("/token",status_code = status.HTTP_200_OK,responses = {**response_status_code})
async def account_token(request : Request,user_id : str ,password : Password,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    request = convert_binary_to_string(request)
    password = password.password
    query = {USER_ID:user_id}
    user = await find_one(db = db,collection = USERS ,query = query)
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    user= dict(user) 
    verify_password(password,user[PASSWORD])
    data = {
        USER_ID : user[USER_ID],
        NICKNAME : user[NICKNAME],
        USAGE : ACCOUNT,
    }
    account_token = encode_access_token(request = request,data = data)
    return account_token



@router.post("/reset_password",responses = {**response_status_code})
async def reset_password(request:Request,token : str,password : Password,
                         db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    request = convert_binary_to_string(request)
    decoded_token = decode_jwt_token(token)
    query = {
        USER_ID:decoded_token.get(USER_ID)
        }
    user = await find_one(db = db,collection = "users",query = query)
    #verify_client_ip(decoded_token = decoded_token,request = request)
    verify_usage(decoded_token = decoded_token,usage = ACCOUNT)
    password = password.password 
    find_query = {
        USER_ID : decoded_token.get(USER_ID)
    }
    modify_query = {
        PASSWORD : pwd_context.hash(password)
    }
    result = await find_one_and_update(db,"users",find_query,modify_query)
    return 




