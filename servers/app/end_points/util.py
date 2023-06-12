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
    request = convert_binary_to_string(request)
    data = {
        CLIENT_IP:request["headers"]["x-real-ip"] if request["headers"].get("x-real-ip") else request["client"][0],
        EMAIL : email.dict().get(EMAIL),
        USAGE : EMAIL
    }
    encoded_jwt_token = encode_access_token(request = request,data = data,expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES)
    html = f"""<p>Hi this CODE PLANET test mail, thanks for using CODE PLANET <br></br>
        TOKEN : {encoded_jwt_token}
        
    </p> """
    message = MessageSchema(
        subject = "CODE PLANET VERFICATION MAIL",
        recipients = [email.dict().get(EMAIL)],
        body = html,
        subtype = MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code = status.HTTP_200_OK, content={"message": "email has been sent"})




