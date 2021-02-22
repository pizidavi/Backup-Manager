import os.path
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

# import control.logger as logging
# from control.Config import Config
from gui.modal import Modal
from gui.view import GUI
from obj.Path import Path


class App:

    def __init__(self, width=500, height=400):
        self.__root = Tk()
        self.__root.title("Backup Manager")
        self.__root.resizable(False, False)
        self.__root.geometry(str(width) + "x" + str(height))

        self.__view = GUI(self.__root)

        # Set default
        self.__view.VOrigin.set(os.getcwd())

        # Set commands
        self.__view.BOrigin.config(command=lambda: self.__get_directory(self.__view.VOrigin))
        self.__view.BBackup.config(command=lambda: self.__get_directory(self.__view.VBackup))
        self.__view.BStart.config(command=self.__start)

        self.__modal = Modal(self.__view.TLog)

        self.__root.mainloop()

    @staticmethod
    def __get_directory(element) -> None:
        folder = filedialog.askdirectory()
        if folder != '':
            element.set(folder)

    def __start(self) -> None:
        origin_dir = Path(self.__view.VOrigin.get())
        backup_dir = Path(self.__view.VBackup.get())

        if not os.path.exists(origin_dir.path) or not os.path.isdir(origin_dir.path):
            messagebox.showerror('Error', 'Origin folder not found')
            return
        if not os.path.exists(backup_dir.path) or not os.path.isdir(backup_dir.path):
            messagebox.showerror('Error', 'Backup folder not found')
            return

        self.__view.TLog.delete(1.0, END)
        self.__modal.backup(origin_dir, backup_dir)
        messagebox.showinfo(message='Completed')
