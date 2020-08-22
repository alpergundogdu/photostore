from datetime import datetime
from os import listdir, makedirs, path, remove

from fastapi import UploadFile
from starlette.responses import FileResponse


class Store():
    """JPG file store"""

    def __init__(self, working_dir: str, backup_dir: str):
        self.working_dir = working_dir
        self.backup_dir = backup_dir
        makedirs(working_dir, exist_ok=True)
        makedirs(backup_dir, exist_ok=True)

    def upload(self, uploaded: UploadFile):
        filename = str(datetime.timestamp(datetime.now())
                       ).replace('.', '') + '.jpg'
        content = uploaded.file.read()
        with open(path.join(self.working_dir, filename), 'wb') as new:
            new.write(content)
        with open(path.join(self.backup_dir, filename), 'wb') as backup:
            backup.write(content)

    def delete(self, filename: str):
        full_path = path.join(self.working_dir, filename)
        if path.exists(full_path):
            remove(full_path)
            return True
        return False

    def list(self):
        return [f for f in listdir(self.working_dir) if f.endswith(".jpg")]

    def read(self, filename):
        full_path = path.join(self.working_dir, filename)
        if path.exists(full_path):
            return FileResponse(path.join(self.working_dir, filename))
        return None
