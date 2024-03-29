from flask import Flask
from flask import request
import logging


log = logging.getLogger()
log.setLevel(logging.ERROR)

app = Flask(__name__)


def custom_read_f():
    return {"message": [x for x in range(100) if x % 5 == 0]}


def custom_write_f(request):
    return {"message": "y" if request['sub_text'] in request['text'] else 'n'}


@app.route("/simple_read", methods=['GET'])
async def simple_read():
    return {"message": "x"}


@app.route("/simple_write", methods=['POST'])
async def simple_write():
    try:
        assert request.get_json()['name'] == 'x'
    except AssertionError:
        return {"message": "n"}
    return {"message": "y"}


@app.route("/custom_read", methods=['GET'])
async def custom_read():
    return custom_read_f()


@app.route("/custom_write", methods=['POST'])
async def custom_write():
    return custom_write_f(request.get_json())


@app.route("/simple_read_sync", methods=['GET'])
def simple_read_sync():
    return {"message": "x"}


@app.route("/simple_write_sync", methods=['POST'])
def simple_write_sync():
    try:
        assert request.get_json()['name'] == 'x'
    except AssertionError:
        return {"message": "n"}
    return {"message": "y"}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8082)
