from tkinter import *


class GUI:

    def __init__(self, root):
        self.__root = root

        self.VOrigin = StringVar()
        self.EOrigin = Entry(self.__root, state='readonly', textvariable=self.VOrigin)
        self.EOrigin.place(relx=0.06, rely=0.05, height=20, relwidth=0.748)

        self.BOrigin = Button(self.__root, text='...', background="#d9d9d9")
        self.BOrigin.place(relx=0.84, rely=0.05, height=24, width=57)

        self.VBackup = StringVar()
        self.EBackup = Entry(self.__root, state='readonly', textvariable=self.VBackup)
        self.EBackup.place(relx=0.06, rely=0.125, height=20, relwidth=0.748)

        self.BBackup = Button(self.__root, text='...', background='#d9d9d9')
        self.BBackup.place(relx=0.84, rely=0.123, height=24, width=57)

        frame = Frame(root)
        frame.place(relx=0.06, rely=0.225, height=250, relwidth=0.888)

        yscrollbar = Scrollbar(frame)
        yscrollbar.pack(side=RIGHT, fill=Y)
        xscrollbar = Scrollbar(frame, orient=HORIZONTAL)
        xscrollbar.pack(side=BOTTOM, fill=X)

        self.TLog = Text(frame, wrap=NONE, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        self.TLog.edit_modified(0)
        self.TLog.bind('<Key>', lambda x: 'break')
        self.TLog.bind('<<Modified>>', lambda x: self.__to_end(self.TLog))
        self.TLog.pack()
        xscrollbar.config(command=self.TLog.xview)
        yscrollbar.config(command=self.TLog.yview)

        self.BStart = Button(self.__root, text='Start', font="-family {Segoe UI} -size 11", background="#d9d9d9")
        self.BStart.place(relx=0.32, rely=0.875, height=34, width=167)

    @staticmethod
    def __to_end(element):
        element.see(END)
        element.edit_modified(0)
