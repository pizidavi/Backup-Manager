import os.path
import shutil
from tkinter import INSERT

from control.Config import Config
from obj.Path import Path
from obj.File import File

config = Config()


class Modal:

    def __init__(self, logger):
        self.__logger = logger

    def backup(self, original_dir, backup_dir):
        trash_dir = Path(os.path.join(backup_dir.path, config.backup_trash_dir.name))
        stats = {
            'new': 0,
            'changed': 0,
            'exists': 0,
            'deleted': 0,
            'error': 0
        }

        if not os.path.exists(trash_dir.path) or not os.path.isdir(trash_dir.path):
            os.mkdir(trash_dir.path)
            self.__logger.insert(INSERT, 'Trash directory created' + '\n')

        for current_dir_path, dirs, files in os.walk(original_dir.path):
            dirs[:] = [d for d in dirs if d not in config.folders_ignore]
            self.__logger.insert(INSERT, 'Checking "{}" folder: {} files'.format(current_dir_path, len(files)) + '\n')
            self.__logger.insert(INSERT, current_dir_path + '\n')

            generic_dir_path = current_dir_path.replace(original_dir.path, '', 1)
            for file in files:
                original = File(file, original_dir.path + generic_dir_path)
                backup = File(file, backup_dir.path + generic_dir_path)
                trash = File(file, trash_dir.path + generic_dir_path)

                if backup.exists and original.last_edit_date == backup.last_edit_date:  # Exists
                    stats['exists'] += 1

                elif backup.exists and original.last_edit_date != backup.last_edit_date:  # Changed
                    if original.last_edit_date > backup.last_edit_date:
                        self.__logger.insert(INSERT, '{}  updated'.format(file) + '\n')
                        stats['changed'] += 1

                        if config.soft_delete:
                            if not os.path.exists(trash.path):
                                os.makedirs(trash.path)
                            elif trash.exists:
                                os.remove(trash.filepath)
                            shutil.move(backup.filepath, trash.path)
                        else:
                            os.remove(backup.filepath)

                        shutil.copy2(original.filepath, backup.path)

                    elif original.last_edit_date < backup.last_edit_date:
                        self.__logger.insert(INSERT, '{}  Original older than Backup!'.format(file) + '\n')
                        stats['error'] += 1

                elif not backup.exists:  # New
                    self.__logger.insert(INSERT, '{} saved'.format(file) + '\n')
                    stats['new'] += 1

                    if not os.path.exists(backup.path):
                        os.makedirs(backup.path)
                    shutil.copy2(original.filepath, backup.path)

                else:
                    self.__logger.insert(INSERT, 'Option not operated: {}'.format(file) + '\n')
                    stats['error'] += 1

        self.__logger.insert(INSERT, 'Checking for deleted file...' + '\n')

        for current_dir_path, dirs, files in os.walk(backup_dir.path):
            dirs[:] = [d for d in dirs if d not in config.folders_ignore]
            # logger.debug('Checking "%s" folder (%s files)', current_dir_path, len(files))

            generic_dir_path = current_dir_path.replace(backup_dir.path, '', 1)
            for file in files:
                original = File(file, original_dir.path + generic_dir_path)
                backup = File(file, backup_dir.path + generic_dir_path)
                trash = File(file, trash_dir.path + generic_dir_path)

                if not original.exists:  # Original file deleted
                    self.__logger.insert(INSERT, '{} {}'.format(file, (
                        'moved to Trash folder' if config.soft_delete else 'deleted')) + '\n')
                    stats['deleted'] += 1

                    if config.soft_delete:
                        if not os.path.exists(trash.path):
                            os.makedirs(trash.path)
                        elif trash.exists:
                            os.remove(trash.filepath)
                        shutil.move(backup.filepath, trash.path)
                    else:
                        os.remove(backup.filepath)

                    if len(os.listdir(backup.path)) == 0:  # remove empty folder
                        self.__logger.insert(INSERT, 'Empty folder "{}" removed'.format(backup.path) + '\n')
                        os.rmdir(backup.path)

        report = "Report | New: {}, Changed: {}, Exists: {}, Deleted: {}, Error: {}".format(
                    stats['new'],
                    stats['changed'],
                    stats['exists'],
                    stats['deleted'],
                    stats['error'])
        self.__logger.insert(INSERT, report + '\n')
        self.__logger.insert(INSERT, 'Complete' + '\n')
