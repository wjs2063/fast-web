from fastapi import FastAPI,Request
from app.api import api_router
import os

main_app = FastAPI()
main_app.include_router(api_router)



@main_app.get("/")
async def main(request: Request):
    return "hello World!"