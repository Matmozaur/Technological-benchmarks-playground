from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class BaseItem(BaseModel):
    name: str


@app.get("/simple_read")
async def simple_read():
    return {"message": "x"}


@app.post("/simple_write")
async def simple_write(request: BaseItem):
    try:
        assert request.name == 'x'
    except AssertionError:
        return {"message": "n"}
    return {"message": "y"}
