import os.path
import shutil
from tkinter import Text, INSERT, END
from tkinter import messagebox

import control.logger as logging
from control.settings import Settings
from obj.Path import Path
from obj.File import File

logger = logging.get_logger(__name__)
settings = Settings()


class Modal:

    def __init__(self, view: Text):
        self.__view = view

    def backup(self, original_dir, backup_dir):
        self.__clear()
        trash_dir = Path(os.path.join(backup_dir.path, settings['SETTINGS']['trash_dir_name']))
        stats = {
            'new': 0,
            'changed': 0,
            'exists': 0,
            'deleted': 0,
            'error': 0
        }

        if not os.path.exists(trash_dir.path) or not os.path.isdir(trash_dir.path):
            os.mkdir(trash_dir.path)
            self.__log('Trash directory created')

        for current_dir_path, dirs, files in os.walk(original_dir.path):
            dirs[:] = [d for d in dirs if d not in settings.folders_ignore]
            self.__log('Checking "{}" folder: {} files'.format(current_dir_path, len(files)))

            generic_dir_path = current_dir_path.replace(original_dir.path, '', 1)
            for file in files:
                original = File(file, original_dir.path + generic_dir_path)
                backup = File(file, backup_dir.path + generic_dir_path)
                trash = File(file, trash_dir.path + generic_dir_path)

                if backup.exists and original.last_edit_date == backup.last_edit_date:  # Exists
                    stats['exists'] += 1

                elif backup.exists and original.last_edit_date != backup.last_edit_date:  # Changed
                    if original.last_edit_date > backup.last_edit_date:
                        self.__log('{}  updated'.format(file))
                        stats['changed'] += 1

                        if settings['SETTINGS']['soft-delete']:
                            if not os.path.exists(trash.path):
                                os.makedirs(trash.path)
                            elif trash.exists:
                                os.remove(trash.filepath)
                            shutil.move(backup.filepath, trash.path)
                        else:
                            os.remove(backup.filepath)

                        shutil.copy2(original.filepath, backup.path)

                    elif original.last_edit_date < backup.last_edit_date:
                        self.__log('{}  Original older than Backup!'.format(file), 40)
                        stats['error'] += 1

                elif not backup.exists:  # New
                    self.__log('{} saved'.format(file))
                    stats['new'] += 1

                    if not os.path.exists(backup.path):
                        os.makedirs(backup.path)
                    shutil.copy2(original.filepath, backup.path)

                else:
                    self.__log('Option not operated: {}'.format(file), 30)
                    stats['error'] += 1

        self.__log('Checking for deleted file...')

        for current_dir_path, dirs, files in os.walk(backup_dir.path):
            dirs[:] = [d for d in dirs if d not in settings.folders_ignore]
            self.__log('Checking "{}" folder ({} files)'.format(current_dir_path, len(files)), 10)

            generic_dir_path = current_dir_path.replace(backup_dir.path, '', 1)
            for file in files:
                original = File(file, original_dir.path + generic_dir_path)
                backup = File(file, backup_dir.path + generic_dir_path)
                trash = File(file, trash_dir.path + generic_dir_path)

                if not original.exists:  # Original file deleted
                    self.__log('{} {}'.format(file, ('moved to Trash folder'
                                                        if settings['SETTINGS']['soft-delete'] else 'deleted')))
                    stats['deleted'] += 1

                    if settings['SETTINGS']['soft-delete']:
                        if not os.path.exists(trash.path):
                            os.makedirs(trash.path)
                        elif trash.exists:
                            os.remove(trash.filepath)
                        shutil.move(backup.filepath, trash.path)
                    else:
                        os.remove(backup.filepath)

                    if len(os.listdir(backup.path)) == 0:  # remove empty folder
                        self.__log('Empty folder "{}" removed'.format(backup.path))
                        os.rmdir(backup.path)

        report = "Report | New: {}, Changed: {}, Exists: {}, Deleted: {}, Error: {}".format(
                    stats['new'],
                    stats['changed'],
                    stats['exists'],
                    stats['deleted'],
                    stats['error'])
        self.__log(report)
        self.__log('Complete')

        messagebox.showinfo(message='Completed')

    def __log(self, text, level=20):
        if level >= 10:
            self.__view.insert(INSERT, text + '\n')
        logger.log(level, text)

    def __clear(self):
        self.__view.delete(1.0, END)
