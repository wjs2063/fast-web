from models.database import *
from main import main_app
import pytest
from fastapi.testclient import TestClient
import httpx


async def overrideSyncdb():
    db = MongoClient(LOCAL_TEST)
    try:
        yield db.local
    finally:
        db.close()




