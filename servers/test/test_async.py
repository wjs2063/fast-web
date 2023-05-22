import pytest
from httpx import AsyncClient
from main import app
from models.database import *
import asyncio
import json
"""
This is a async Test File 
"""




base_url = "http://172.30.1.56:54999"


async def override_async_db():
    db = motor_asyncio.AsyncIOMotorClient(PUBLIC_TEST)
    #db.get_io_loop = asyncio.get_event_loop
    try :
        yield db.local
    finally :
        db.close()

app.dependency_overrides[asyncdb] = override_async_db


@pytest.mark.asyncio
async def test_create_user():
    db = motor_asyncio.AsyncIOMotorClient(PUBLIC_TEST)
    db.local.users.drop()
    #db.users.drop()
    async with AsyncClient(app = app,base_url = base_url)  as ac:
        response = await ac.post("/api/user",
            headers = {"Content-Type": "application/json"},
            json = {"name": "jaehyeon",
               "user_id": "aaa1234",
               "email": "kkk@naver.com",
               "password": "1234567",
               "nickname": "user1",
               "disabled": "False"
                }
        )
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app = app,base_url = base_url)  as ac:
        response = await ac.post("/api/login",
            headers = {'Content-Type':  'application/x-www-form-urlencoded'},
            content = 'grant_type=&username=aaa1234&password=1234567&scope=&client_id=&client_secret='
             )

    assert response.status_code == 200

    async with AsyncClient(app = app,base_url = base_url)  as ac:
        response = await ac.post("/api/login",
            headers = {'Content-Type':  'application/x-www-form-urlencoded'},
            content = 'grant_type=&username=whoareyou&password=1234567&scope=&client_id=&client_secret='
            )
    assert  response.status_code == 401
