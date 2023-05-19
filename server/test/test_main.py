from fastapi import FastAPI,Depends
from server.model.database import *
from main import app

from fastapi.testclient import TestClient
from typing import Annotated



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






