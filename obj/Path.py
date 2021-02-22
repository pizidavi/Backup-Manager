import os.path


class Path:

    def __init__(self, path: str):
        self.__path = os.path.join(path.replace('/', '\\'), '')
        self.__name = os.path.basename(os.path.dirname(self.__path))

    @property
    def path(self):
        return self.__path

    @property
    def name(self):
        return self.__name if self.__name != '' else 'root'
