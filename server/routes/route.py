from fastapi import *
from fastapi.responses import *
from typing import Annotated
from ..model.database import *
from fastapi.staticfiles import StaticFiles
apps = APIRouter()
apps.mount("/templates/",StaticFiles(directory = "/web/server/templates/static",html = True),name = "static")

@apps.post("/api")
async def test(db: Annotated[MongoClient ,Depends(get_db)]):
    db.user.insert_one({"example":1})
    return "hello World!"

@apps.get("/")
async def main():
    return FileResponse("/web/server/templates/static/index.html")
