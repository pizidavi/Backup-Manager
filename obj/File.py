import os.path
from datetime import datetime


class File:

    def __init__(self, filename: str, path: str):
        self.__filename = filename
        self.__filepath = os.path.join(path, filename)
        self.__path = path

    @property
    def filename(self) -> str:
        return self.__filename

    @property
    def filepath(self) -> str:
        return self.__filepath

    @property
    def path(self) -> str:
        return self.__path

    @property
    def exists(self) -> bool:
        return os.path.exists(self.__filepath)

    @property
    def last_edit_date(self):
        if self.exists:
            return datetime.fromtimestamp(int(os.path.getmtime(self.__filepath)))
        else:
            return None
