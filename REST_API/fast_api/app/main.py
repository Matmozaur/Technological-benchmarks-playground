from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class BaseItem(BaseModel):
    name: str


class CustomItem(BaseModel):
    text: str
    sub_text: str


def custom_read_f():
    return {"message": [x for x in range(100) if x % 5 == 0]}


def custom_write_f(request: CustomItem):
    return {"message": "y" if request.sub_text in request.text else 'n'}


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


@app.get("/custom_read")
async def custom_read():
    return custom_read_f()


@app.post("/custom_write")
async def custom_write(request: CustomItem):
    return custom_write_f(request)


@app.get("/simple_read_sync")
def simple_read_sync():
    return {"message": "x"}


@app.post("/simple_write_sync")
def simple_write_sync(request: BaseItem):
    try:
        assert request.name == 'x'
    except AssertionError:
        return {"message": "n"}
    return {"message": "y"}
