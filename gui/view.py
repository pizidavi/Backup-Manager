from tkinter import *


class View:

    def __init__(self, root: Tk):
        self.__root = root
        self.__root.title('Backup Manager')
        self.__root.iconbitmap('assets/icon.ico')
        self.__root.wm_minsize(width=450, height=400)
        self.__root.wm_maxsize(width=700, height=420)
        self.__root.geometry('500x400')

        Label(self.__root, text='Original Folder').place(relx=0.04, rely=0.01, height=20, width=100)
        self.VOrigin = StringVar()
        self.EOrigin = Entry(self.__root, textvariable=self.VOrigin)
        self.EOrigin.place(relx=0.06, rely=0.06, height=20, relwidth=0.748)

        self.BOrigin = Button(self.__root, text='...', background="#d9d9d9")
        self.BOrigin.place(relx=0.84, rely=0.055, height=24, width=57)

        Label(self.__root, text='Backup Folder').place(relx=0.04, rely=0.120, height=20, width=100)
        self.VBackup = StringVar()
        self.EBackup = Entry(self.__root, textvariable=self.VBackup)
        self.EBackup.place(relx=0.06, rely=0.17, height=20, relwidth=0.748)

        self.BBackup = Button(self.__root, text='...', background='#d9d9d9')
        self.BBackup.place(relx=0.84, rely=0.163, height=24, width=57)

        Label(self.__root, text='Log').place(relx=0.04, rely=0.232, height=20, width=45)
        frame = Frame(root)
        yscrollbar = Scrollbar(frame)
        yscrollbar.pack(side=RIGHT, fill=Y)
        xscrollbar = Scrollbar(frame, orient=HORIZONTAL)
        xscrollbar.pack(side=BOTTOM, fill=X)

        self.TLog = Text(frame, wrap=NONE, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        self.TLog.edit_modified(0)
        self.TLog.bind('<Key>', lambda x: None if x.state == 12 and (x.keycode == 67 or x.keycode == 65) else 'break')
        self.TLog.bind('<<Modified>>', lambda x: self.__to_end(self.TLog))
        self.TLog.pack(fill=BOTH)
        xscrollbar.config(command=self.TLog.xview)
        yscrollbar.config(command=self.TLog.yview)
        frame.place(relx=0.06, rely=0.285, height=230, relwidth=0.888)

        self.BStart = Button(self.__root, text='Start', font="-family {Segoe UI} -size 11", background="#d9d9d9")
        self.BStart.place(relx=0.32, rely=0.875, height=34, width=167)

    @staticmethod
    def __to_end(element: Text):
        element.see(END)
        element.edit_modified(0)
