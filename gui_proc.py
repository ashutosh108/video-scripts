import tkinter as tk
from tkinter import ttk
import os


class ProcessingFrame:
    frame = None  # type: ttk.LabelFrame
    orig_button = None  # type: ttk.Button
    parent = None  # type: ttk.Frame
    filename_var = None  # type: tk.StringVar

    def __init__(self, parent_frame: ttk.Frame, filename_var: tk.StringVar):
        super().__init__()
        self.parent = parent_frame
        self.filename_var = filename_var
        self.frame = ttk.LabelFrame(parent_frame, text='Processing')

        ttk.Label(self.frame, text='Orig:').grid(row=0, column=0)
        self.orig_button = ttk.Button(self.frame, text='Run', command=self.orig_run)
        self.orig_button.grid(row=0, column=1)

    def orig_run(self):
        dir = os.path.dirname(__file__)
        path = os.path.join(dir, 'orig.cmd')
        filename = self.filename_var.get()
        cmd_str = 'start cmd /c ' + path + ' ' + '"' + filename + '"'
        print(cmd_str)
        os.system(cmd_str)
