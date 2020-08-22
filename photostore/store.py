from os import listdir, makedirs, path, remove

from fastapi import UploadFile
from datetime import datetime
from starlette.responses import FileResponse

class Store():
    """JPG file store"""

    def __init__(self, working_dir: str):
        self.working_dir = working_dir
        makedirs(working_dir, exist_ok = True)

    def upload(self, uploaded: UploadFile):
        filename = str(datetime.timestamp(datetime.now())).replace('.', '') + '.jpg'
        with open(path.join(self.working_dir, filename), 'wb') as new:
            new.write(uploaded.file.read())

    def delete(self, filename: str):
        remove(filename)

    def list(self):
        return [f for f in listdir(self.working_dir) if f.endswith(".jpg")]

    def read(self, filename):
        return FileResponse(path.join(self.working_dir, filename))
