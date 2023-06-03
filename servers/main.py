from fastapi import FastAPI,Request
from app.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from configs.constant import *
import os

main_app = FastAPI()
main_app.include_router(api_router)
origins = [
    os.environ["ALLOW_ORIGIN_1"],
    os.environ["ALLOW_ORIGIN_2"],
    os.environ["ALLOW_ORIGIN_3"]
]

main_app.add_middleware(
    CORSMiddleware,
    allow_origins = origins, 
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@main_app.get("/")
async def main(request: Request):
    return "hello World!"
