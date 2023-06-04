from fastapi import *
from fastapi.responses import *
from typing import Annotated
from models.database import *
from schemas.token import *
from fastapi.staticfiles import StaticFiles
from configs.constant import *
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from configs.security import *
from passlib.context import CryptContext
from datetime import datetime,timedelta
from schemas.userSchema import *
from bson import ObjectId
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
import os
from schemas.token import *
from email.mime.text import MIMEText
from schemas.mailSchema import *
from typing import Annotated
from models.database import *

router = APIRouter()



@router.post("/register/email")
async def simple_send(request:Request,email: EmailSchema) -> JSONResponse:
    data = {
        "client_ip" : request.client.host,
        "email" : email.dict().get("email"),
        "token_type" : "email"
    }
    encoded_jwt_token = encode_access_token(data,expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES)
    html = f"""<p>Hi this CODE PLANET test mail, thanks for using CODE PLANET <br></br>
        TOKEN : {encoded_jwt_token}
        
    </p> """
    message = MessageSchema(
        subject = "Fastapi-Mail module",
        recipients = [email.dict().get("email")],
        body = html,
        subtype = MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code = status.HTTP_200_OK, content={"message": "email has been sent"})




