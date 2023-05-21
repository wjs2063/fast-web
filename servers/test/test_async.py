import pytest
from httpx import AsyncClient
from main import app
from models.database import *
import asyncio
"""
This is a async Test File 
"""




base_url = "http://172.30.1.56:54321"


async def override_async_db():
    db = motor_asyncio.AsyncIOMotorClient(TEST_MONGODB)
    db.get_io_loop = asyncio.get_event_loop
    try :
        yield db.local
    finally :
        db.close()

app.dependency_overrides[asyncdb] = override_async_db


@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app = app,base_url = base_url)  as ac:
        response = await ac.post("/api/user",
    json = {"name": "jaehyeon",
       "user_id": "aaa1234",
       "email": "kkk@naver.com",
       "password": "1234567",
       "nickname": "user1",
       "disabled": "False"
    }
    )
    assert response.status_code == 201

