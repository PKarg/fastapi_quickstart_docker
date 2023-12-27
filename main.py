from fastapi import FastAPI

from db.setup import Base, engine
from models.users import User

Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "Hello World"}
