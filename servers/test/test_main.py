from models.database import *
from main import app

from fastapi.testclient import TestClient


async def overrideget_db():
    db = MongoClient(TEST_MONGODB)
    try:
        yield db.local
    finally:
        db.close()


# for test_db
app.dependency_overrides[get_db] = overrideget_db
client = TestClient(app)

def test():
    response = client.post("/api",
                json = {}
                )
    assert response.status_code == 200
    assert response.json() == "hello World!"



def test_createUser():
    response = client.post("/api/user",
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

