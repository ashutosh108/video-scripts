import tkinter as tk
from tkinter import ttk
import os

import audition
import meta


class ProcessingFrame:
    frame = None  # type: ttk.LabelFrame
    orig_button = None  # type: ttk.Button
    parent = None  # type: ttk.Frame
    filename_var = None  # type: tk.StringVar
    rus_button = None  # type: ttk.Button
    timing_button = None  # type: ttk.Button
    hk_button = None  # type: ttk.Button

    def __init__(self, parent_frame: ttk.Frame, filename_var: tk.StringVar):
        super().__init__()
        self.parent = parent_frame
        self.filename_var = filename_var
        self.frame = ttk.LabelFrame(parent_frame, text='Processing')

        ttk.Label(self.frame, text='Orig:').grid(row=0, column=0)
        self.orig_button = ttk.Button(self.frame, text='Run', command=self.orig_run)
        self.orig_button.grid(row=0, column=1)

        ttk.Label(self.frame, text='Rus:').grid(row=1, column=0)
        self.rus_button = ttk.Button(self.frame, text='Rus', command=self.rus_run)
        self.rus_button.grid(row=1, column=1)

        ttk.Label(self.frame, text='Timing:').grid(row=2, column=0)
        self.timing_button = ttk.Button(self.frame, text='Get', command=self.timing_run)
        self.timing_button.grid(row=2, column=1)

        ttk.Label(self.frame, text='Hk.ru:').grid(row=3, column=0)
        self.hk_button = ttk.Button(self.frame, text='Get code', command=self.hk_run)
        self.hk_button.grid(row=3, column=1)

    def orig_run(self):
        dir = os.path.dirname(__file__)
        path = os.path.join(dir, 'orig.cmd')
        filename = self.filename_var.get()
        cmd_str = 'start cmd /c ' + path + ' ' + '"' + filename + '"'
        print(cmd_str)
        os.system(cmd_str)

    def rus_run(self):
        dir = os.path.dirname(__file__)
        path = os.path.join(dir, 'rus.cmd')
        filename = self.filename_var.get()
        cmd_str = 'start cmd /c ' + path + ' ' + '"' + filename + '"'
        print(cmd_str)
        os.system(cmd_str)

    def timing_run(self):
        text = audition.timestamps(self.filename_var.get())
        self.parent.clipboard_clear()
        self.parent.clipboard_append(text)

    def hk_run(self):
        text = meta.get_hk_code(self.filename_var.get())
        self.parent.clipboard_clear()
        self.parent.clipboard_append(text)
