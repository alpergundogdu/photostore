#!/usr/bin/python3

from datetime import datetime
from os import environ
from typing import List

from fastapi import FastAPI, File, HTTPException, Request, UploadFile, status
from fastapi.templating import Jinja2Templates

from .auth import Auth
from .store import Store

app = FastAPI()

store = Store(environ["WORKING_DIR"], environ["BACKUP_DIR"])
auth = Auth(environ["SECRET_KEYS_FILE"])

templates = Jinja2Templates(directory='templates')

def get_date(filename):
    return str(datetime.utcfromtimestamp(int(filename.split(".")[0]) / 1000000))


def convert_list(filenames: List[str]):
    return [{
        "filename": item,
        "date": get_date(item)
    } for item in sorted(filenames, reverse=True)]


@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse(
        "list.html",
        {"request": request, "list": convert_list(store.list()), "root": "automato"})

@app.get("/list.rss")
async def list_rss(request: Request):
    return templates.TemplateResponse(
        "rss.template",
        {"request": request, "list": convert_list(store.list()), "root": "automato"})

@app.get("/list")
async def list_photos():
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
