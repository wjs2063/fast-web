import pytest
from fastapi import *
from httpx import AsyncClient
from main import main_app
from models.database import *
import asyncio
import json
import os
from configs.constant import *
"""
This is a async Test File 
"""




base_url = "https://www.codeplanet.site"


async def override_async_db():
    db = motor_asyncio.AsyncIOMotorClient(PUBLIC_TEST)
    try :
        yield db.local
    finally :
        db.close()

main_app.dependency_overrides[asyncdb] = override_async_db



@pytest.mark.asyncio
async def test_reset():
    pass

@pytest.mark.asyncio
async def test_create_user():
    db = motor_asyncio.AsyncIOMotorClient(PUBLIC_TEST)
    await db.local.users.drop()
    await db.local.token.drop()
    async with AsyncClient(app = main_app,base_url = base_url)  as ac:
        response = await ac.post("/api/auth/sign-up",
            headers = {"Content-Type": "application/json",
                       "accept": "application/json"
                       },
            content = json.dumps({
                "user": {
                    "name": "jaehyeon",
                    "user_id": "aaa1234",
                    "email": "jahy5352@naver.com",
                    "gender": "남자",
                    "password": "1234567",
                    "nickname": "user1",
                    "birth_year": 1900,
                    "birth_month": 5,
                    "birth_day": 25,
                    "disabled": True
                },
                "token": {
                    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaXAiOiI1OS4xOC4yNDMuMTY2IiwiZW1haWwiOiJqYWh5NTM1MkBuYXZlci5jb20iLCJ0b2tlbl90eXBlIjoiZW1haWwiLCJpYXQiOjE2ODU4NzIyNjAsImV4cCI6MTcwNDAxNjI2MH0.z3gfihq7Yhu6s346mfZH8AnGoOG0jYuNf8z_S80hJuk"
                }
            }
            )
        )
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app = main_app,base_url = base_url)  as ac:
        response = await ac.post("/api/auth/login",
            headers = {'Content-Type':  'application/x-www-form-urlencoded',},
            content = 'grant_type=&username=aaa1234&password=1234567&scope=&client_id=&client_secret='
             )

    assert response.status_code == status.HTTP_200_OK

    async with AsyncClient(app = main_app,base_url = base_url)  as ac:
        response = await ac.post("/api/auth/login",
            headers = {'Content-Type':  'application/x-www-form-urlencoded'},
            content = 'grant_type=&username=whoareyou&password=1234567&scope=&client_id=&client_secret='
            )
    assert  response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_duplicate_userId():
    async with AsyncClient(app = main_app, base_url = base_url) as ac:
        response = await ac.get("/api/auth/userId?user_id=aaa1234",
                                 #headers = {'Content-Type':  'application/x-www-form-urlencoded'},
                                 #content = "user_id=aaa1234"
                                 )
    assert response.status_code == status.HTTP_409_CONFLICT

    async with AsyncClient(app = main_app, base_url = base_url) as ac:
        response = await ac.get("/api/auth/userId?user_id=aaa12345",
                                 #headers = {'Content-Type':  'application/x-www-form-urlencoded'},
                                 #content = "user_id=aaa12345"
                                 )
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_duplicate_email():
    async with AsyncClient(app = main_app,base_url = base_url) as ac:
        response = await ac.get("/api/auth/email?email_str=jahy5352%40naver.com",
                                 #headers = {'Content-Type': 'application/x-www-form-urlencoded'},
                                 #content = "email_str=kkk%40naver.com'"
                                )
    assert response.status_code == status.HTTP_409_CONFLICT

    async with AsyncClient(app = main_app,base_url = base_url) as ac:
        response = await ac.get("/api/auth/email?email_str=kkk1%40naver.com",
                                 #headers = {'Content-Type':  'application/x-www-form-urlencoded'},
                                 #content = "email_str=kkk%40naver.com'"
                                 )
    assert response.status_code == status.HTTP_200_OK







@pytest.mark.asyncio
async def test_validate_token():
    async with AsyncClient(app = main_app,base_url = base_url) as ac :
        response = await ac.get("/api/auth/register/validation?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaXAiOiI1OS4xOC4yNDMuMTY2IiwiZW1haWwiOiJqYWh5NTM1MkBuYXZlci5jb20iLCJ0b2tlbl90eXBlIjoiZW1haWwiLCJpYXQiOjE2ODU4NzEzODksImV4cCI6MTcwNDAxNTM4OX0.pBK9lCcR8WD33UiKH-Sn0m3TmVT1-BHMymo7rxR06gQ")
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_account_token():
    async with AsyncClient(app = main_app,base_url = base_url) as ac:
        response = await ac.post("/api/account/token?user_id=aaa1234",
                                 json = {
                                     "password":"1234567"
                                 }
                                 )
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_logout():
    async with AsyncClient(app = main_app,base_url = base_url)  as ac:
        login_response = await ac.post("/api/auth/login",
            headers = {'Content-Type':  'application/x-www-form-urlencoded',},
            content = 'grant_type=&username=aaa1234&password=1234567&scope=&client_id=&client_secret='
             )
    access_token = login_response.json()["token"]["token"]  
    assert login_response.status_code == status.HTTP_200_OK
    async with AsyncClient(app = main_app,base_url = base_url)  as ac:
            logout_response = await ac.post("/api/auth/logout",
                                            headers = {
                                                "access-token":" eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWFhMTIzNCIsInRva2VuX3R5cGUiOiJsb2dpbiIsImlhdCI6MTY4NjE0NzM1NCwiZXhwIjoxNjg2MTQ5MTU0LCJjbGllbnRfaXAiOiI1OS4xOC4yNDMuMTY2In0.176u2h2-QHJDLdWzZdbjucPYwwiZouGqPp0FzBgMiP4" 
                                            },
                                            json = {}
                                            )
    assert logout_response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_reset_password():
    async with AsyncClient(app = main_app,base_url = base_url) as ac:
        token_response = await ac.post("/api/account/token?user_id=aaa1234",
                            headers = {
                                'Content-Type': 'application/json',
                                'accept': 'application/json'},
                            json = {
                                "password":"1234567"
                            }
                            )
        token = token_response.json()
        response = await ac.post(f"/api/account/reset_password?token={token}",
                                 json = {
                                     "password": "234567"
                                 }
                                 )
        
        assert response.status_code == status.HTTP_200_OK



    

@pytest.mark.asyncio
async def test_generate_access_token():
    pass


@pytest.mark.asyncio
async def test_database_reset():
    pass 

@pytest.mark.asyncio
async def test_get_question_list():
    async with AsyncClient(app = main_app,base_url = base_url) as ac:
        login_response = await ac.post("/api/auth/login",
                                    headers = {
                                    'accept': 'application/json',
                                    'Content-Type': 'application/x-www-form-urlencoded'

                                    },
                                content = 
                                    'grant_type=&username=aaa1234&password=234567&scope=&client_id=&client_secret='
                                
                                    )
        assert login_response.status_code == status.HTTP_200_OK
        access_token = login_response.json()["token"]["token"]

        response = await ac.get("/api/user/question",
                                 headers = {
                                     "access-token" : access_token
                                     
                                 }
                                 )
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_post_question():
    async with AsyncClient(app = main_app,base_url = base_url) as ac:
        login_response = await ac.post("/api/auth/login",
                                 headers = {
                                    'accept': 'application/json',
                                    'Content-Type': 'application/x-www-form-urlencoded'

                                 },
                                content = 
                                    'grant_type=&username=aaa1234&password=234567&scope=&client_id=&client_secret='
                                
                                 )
        assert login_response.status_code == status.HTTP_200_OK
        access_token = login_response.json()["token"]["token"]
        question_post_response = await ac.post("/api/user/question",
                                         headers = {
                                             "access-token":access_token
                                         },
                                         json = {
                                            "user_id": "aaa1234",
                                            "nickname": "test_nick",
                                            "subject": "DFS/BFS Base Code",
                                            "content": "DFS란말이죠?",
                                            "category": "DFS/BFS",
                                            "language": "python",
                                            "is_completed": False
                                            }
                                         )
        assert question_post_response.status_code == status.HTTP_201_CREATED



@pytest.mark.asyncio
async def test_update_question():
    pass

@pytest.mark.asyncio
async def test_delete_question():
    pass