from os import environ

from fastapi import FastAPI, File, UploadFile, HTTPException, status

from .auth import Auth
from .store import Store

app = FastAPI()

SECRET_KEYS_FILE = environ["SECRET_KEYS_FILE"]
WORKING_DIR = environ["WORKING_DIR"]

store = Store(WORKING_DIR)
auth = Auth(SECRET_KEYS_FILE)

@app.get("/")
async def main():
    return store.list()


@app.get("/file/{filename}")
async def read(filename: str):
    content = store.read(filename)
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return content


@app.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload(file: UploadFile = File(...), secret_key: str = ''):
    if not auth.is_valid(secret_key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    store.upload(file)
    return {"result": "success"}


@app.post("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete(filename: str, secret_key: str):
    if not auth.is_valid(secret_key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not store.delete(filename):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"result": "success"}

