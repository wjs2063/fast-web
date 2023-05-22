from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.route import apps
import os

app = FastAPI()
app.include_router(apps)


"""
@app.post("/api")
async def post(db: Annotated[MongoClient ,Depends(get_db)]):
    db.user.insert_one({"example":1})
    return "hello World!"

"""
