import os.path
from threading import Thread
from tkinter import Tk, StringVar
from tkinter import filedialog, messagebox

import control.logger as logging
from control.settings import Settings
from gui.modal import Modal
from gui.view import View
from obj.Path import Path

logger = logging.get_logger(__name__)
settings = Settings()


class App:

    def __init__(self):
        self.__root = Tk()
        self.__view = View(self.__root)
        self.__modal = Modal(self.__view.TLog)

        # Set default
        self.__view.VOrigin.set(settings['DEFAULT_PATH']['original']
                                if settings['DEFAULT_PATH']['original'] else os.getcwd())
        self.__view.VBackup.set(settings['DEFAULT_PATH']['backup'])

        # Set commands
        self.__view.BOrigin.config(command=lambda: self.__get_directory(self.__view.VOrigin))
        self.__view.BBackup.config(command=lambda: self.__get_directory(self.__view.VBackup))
        self.__view.BStart.config(command=self.__start)

        self.__root.mainloop()

    @staticmethod
    def __get_directory(element: StringVar) -> None:
        folder = filedialog.askdirectory()
        if folder != '':
            element.set(folder)

    def __start(self) -> None:
        origin_dir = Path(self.__view.VOrigin.get())
        backup_dir = Path(self.__view.VBackup.get())

        if not os.path.exists(origin_dir.path) or not os.path.isdir(origin_dir.path):
            messagebox.showerror('Error', 'Origin folder not found')
            logger.error('Origin folder not found. Operation aborted')
            return
        if not os.path.exists(backup_dir.path) or not os.path.isdir(backup_dir.path):
            messagebox.showerror('Error', 'Backup folder not found')
            logger.error('Backup folder not found. Operation aborted')
            return

        settings.set('DEFAULT_PATH', 'original', origin_dir.path)
        settings.set('DEFAULT_PATH', 'backup', backup_dir.path)

        Thread(target=self.__modal.backup, args=(origin_dir, backup_dir)).start()
