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
    check_password(password,user_info["password"])
    data = {
        "user_id" : user_id,
        "token_type" : "account",
        "client_ip" : request.client.host
    }
    print(data)
    account_token = create_access_token(data = data)
    return account_token


@router.post("/reset_password",status_code = status.HTTP_200_OK)
async def reset_password(request:Request,token : str,password : Password,
                         db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    decoded_token = decode_jwt_token(token)
    query = {
        "user_id":decoded_token.get("user_id")
        }
    user = await find_one(db,query)
    check_client_ip(decoded_token = decoded_token,request = request)
    check_token_type(decoded_token = decoded_token,token_type = "account")
    password = password.password 
    find_query = {
        "user_id" : decoded_token.get("user_id")
    }
    modify_query = {
        "password" : pwd_context.hash(password)
    }
    result = await find_one_and_update(db,find_query,modify_query)
    return 




