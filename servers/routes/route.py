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
from fastapi.templating import Jinja2Templates
import os
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
apps = APIRouter()

@apps.get("/",response_class=HTMLResponse)
async def main(request: Request):
    return "hello World!"
    #templates.TemplateResponse(f"{os.getcwd()}/templates/static/index.html",{"request":request})


#apps.mount("/templates",StaticFiles(directory = f"{os.getcwd()}/templates/static"),name = "static")
#templates = Jinja2Templates(directory="/templates/static")


#login

@apps.post("/api/login",response_model = Token,status_code = 200)
async def login (request : Request,
                                  form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                  db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)],
                                  ):
    user = await get_user(db,form_data.username)
    if not user :
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "user is not exist",
                            #headers={"WWW-Authenticate": "Bearer"},
                            )
    if not pwd_context.verify(form_data.password,user['password']):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "Invalid password",
                            #headers={"WWW-Authenticate": "Bearer"},
                            )
    # proxy 환경에서 사용하면 로직이 달라짐.
    data = {
        "user_id" : user["user_id"],
        "ip_addr" : request.client.host
    }

    access_token = create_access_token(
        data = data, expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES
    )
    #print(jwt.decode(access_token,SECRETKEY,algorithms = [ALGORITHM]))

    content = {"message" : "fastapi"}
    headers = {"access_token":access_token,"token_type": "bearer"}
    return JSONResponse(content = content,headers = headers)


@apps.post("/api/test")
async def test(db: Annotated[MongoClient ,Depends(get_db)]):
    db.user.insert_one({"example":datetime.utcnow()})
    return "hello World!"


@apps.post("/api/user",response_model = UserData,status_code = 201)
async def create_user_async(user :User,db: Annotated[motor_asyncio.AsyncIOMotorClient ,Depends(asyncdb)]):
    user = dict(user)
    current_user = await get_user(db,user["user_id"])
    if current_user :
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = "이미 존재하는 회원 입니다.")
    user["password"] = pwd_context.hash(user["password"])
    set_datetime(user)
    await db.users.insert_one(user)
    #data = dict(await db.users.find_one(user))
    #serializeId(data)
    return user
