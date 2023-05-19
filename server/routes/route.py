from fastapi import *
from typing import Annotated
from ..model.database import *


apps = APIRouter()



@apps.post("/api")
async def post(db: Annotated[MongoClient ,Depends(get_db)]):
    db.user.insert_one({"example":1})
    return "hello World!"