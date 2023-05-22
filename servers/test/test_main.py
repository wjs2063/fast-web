from models.database import *
from main import app
import pytest
from fastapi.testclient import TestClient
import httpx


async def overrideSyncdb():
    db = MongoClient(TEST_MONGODB)
    try:
        yield db.local
    finally:
        db.close()




