from models.database import *
from main import main_app
import pytest
from fastapi.testclient import TestClient

"""
This is Synchroniaztion Test File
sub_main branch!
"""



async def override_sync_db():
    db = MongoClient(PUBLIC_TEST)
    try:
        yield db.local
    finally:
        db.close()


main_app.dependency_overrides[get_db] = override_sync_db
client = TestClient(main_app)

def test():
    response = client.get("/")
    assert response.status_code == 200

"""
def test_create_user():
    response = client.post("/api/auth/sign-up",
                           json = {"name": "jaehyeon",
                                   "user_id": "aaa1234",
                                   "email": "kkk@naver.com",
                                   "password": "1234567",
                                   "nickname": "user1",
                                   "disabled": "False"}
                           )
    assert response.status_code == 201
    assert response.json() == {
        "name": "jaehyeon",
        "user_id": "aaa1234",
        "email": "kkk@naver.com",
        "nickname": "user1",
        "disabled": False
    }
"""