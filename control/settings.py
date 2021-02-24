import os.path
import configparser

FOLDER = '.BackupManager'
FILENAME = 'settings.ini'
FOLDERS_IGNORE_FILENAME = 'folders.ignore'
LOG_FILENAME = 'syslog.log'

PATH = os.path.join(os.path.expanduser('~'), FOLDER)
FILEPATH = os.path.join(PATH, FILENAME)
FOLDERS_IGNORE_FILEPATH = os.path.join(PATH, FOLDERS_IGNORE_FILENAME)
LOG_FILEPATH = os.path.join(PATH, LOG_FILENAME)

if not os.path.exists(PATH) or not os.path.isdir(PATH):
    os.mkdir(PATH)
if not os.path.exists(FILEPATH) or not os.path.isfile(FILEPATH):
    c = configparser.ConfigParser()
    c['SETTINGS'] = {
        'trash_dir_name': '.trash',
        'soft-delete': True
    }
    c['DEFAULT_PATH'] = {
        'original': '',
        'backup': ''
    }
    c.write(open(FILEPATH, 'w'))
if not os.path.exists(FOLDERS_IGNORE_FILEPATH) or not os.path.isfile(FOLDERS_IGNORE_FILEPATH):
    open(FOLDERS_IGNORE_FILEPATH, 'w').close()


class Settings(configparser.ConfigParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().read(FILEPATH)

        folders_ignore_file = open(FOLDERS_IGNORE_FILEPATH, 'r')
        self.__folders_ignore = [line for line in folders_ignore_file.read().split('\n') if line != '']

        folders_ignore_file.close()

    @property
    def folders_ignore(self):
        return self.__folders_ignore + [super().get('SETTINGS', 'trash_dir_name')]

    def set(self, section, option, value=''):
        old = (super().get(section, option) if super().has_option(section, option) else None)
        if old != value:
            super().set(section, option, value)
            self.__save()

    def __save(self):
        super().write(open(FILEPATH, 'w'))
