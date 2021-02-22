import os
import shutil
import json

from obj.Path import Path

CONFIG_FILENAME = 'config.json'
FOLDERS_IGNORE_FILENAME = 'folders.ignore'


class Config:

    def __init__(self):
        if not os.path.exists(CONFIG_FILENAME):
            if os.path.exists(CONFIG_FILENAME + '.sample'):
                shutil.copy2(CONFIG_FILENAME + '.sample', CONFIG_FILENAME)
            else:
                raise Exception('Missing config.json.sample to creating config file')
        if not os.path.exists(FOLDERS_IGNORE_FILENAME):
            open(FOLDERS_IGNORE_FILENAME, 'w').close()

        config_file = open(CONFIG_FILENAME, 'r')
        folders_ignore_file = open(FOLDERS_IGNORE_FILENAME, 'r')
        self.__config = json.loads(config_file.read())
        self.__folders_ignore = [line for line in folders_ignore_file.read().split('\n') if line != '']

        for key, value in self.__config.items():
            if value == '':
                raise Exception('Missing option "{}" in config.json'.format(key))

        config_file.close()
        folders_ignore_file.close()

    @property
    def original_dir(self) -> Path:
        return Path(self.__config['original_dir'])

    @property
    def backup_dir(self) -> Path:
        return Path(self.__config['backup_dir'])

    @property
    def backup_trash_dir(self) -> Path:
        return Path(os.path.join(self.backup_dir.path, self.__config['backup_trash_dir_name']))

    @property
    def soft_delete(self) -> bool:
        return self.__config['soft-delete']

    @property
    def debug(self) -> bool:
        return self.__config['debug']

    @property
    def folders_ignore(self) -> list:
        return self.__folders_ignore + [self.backup_trash_dir.name]
