from fastapi import FastAPI
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
from fastapi_camelcase import CamelModel


class EmailSchema(CamelModel):
    to: EmailStr
    subject :str
    message : str




