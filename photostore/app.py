from os import environ

from fastapi import FastAPI, File, UploadFile

from .store import Store
from .auth import Auth

app = FastAPI()

SECRET_KEYS_FILE = environ["SECRET_KEYS_FILE"]
WORKING_DIR = environ["WORKING_DIR"]

store = Store(WORKING_DIR)
auth = Auth(SECRET_KEYS_FILE)

@app.get("/")
def main():
    return store.list()


@app.get("/file/{filename}")
def read(filename: str):
    return store.read(filename)


@app.post("/upload")
def upload(file: UploadFile = File(...), secret_key: str = ''):
    if auth.is_valid(secret_key):
        store.upload(file)
        return {"hell": "yeah"}
    return {"hell": "no"}

@app.post("/delete")
def delete(filename: str, secret_key: str):
    if auth.is_valid(secret_key):
        store.delete(filename)
    return {"deletos": "yes"}

