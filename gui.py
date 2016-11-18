import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import meta


class FileFrame():
    frame = None
    filename = None
    lang = None
    lang_frame = None

    def __init__(self, parent_frame):
        self.frame = ttk.LabelFrame(parent_frame, text='Source file: ')
        ttk.Label(self.frame, text="File name:").grid(column=0, row=0, sticky=tk.W)

        self.filename = tk.StringVar()
        self.filename.set('(not selected)')
        filename_entry = ttk.Entry(self.frame, width=60, textvariable=self.filename)
        filename_entry.configure(state='readonly')
        filename_entry.grid(column=1, row=0, sticky=(tk.N, tk.W))

        ttk.Button(self.frame, text='Browse...', command=self.browse_for_file).grid(column=2, row=0)

        self.lang = tk.StringVar()
        self.lang.set('en')
        self.lang.trace('w', lambda *args: self.lang_changed_callback())
        self.lang_frame = ttk.LabelFrame(self.frame, text='Source language:')
        ttk.Radiobutton(self.lang_frame, text='English', variable=self.lang, value='en').grid()
        ttk.Radiobutton(self.lang_frame, text='Russian', variable=self.lang, value='ru').grid()
        self.lang_frame.grid(column=0, row=1, columnspan=3, sticky='nw')
        self.disable_widget(self.lang_frame)

    def disable_widget(self, widget):
        self.set_state_recursive(widget, ['disabled'])

    def enable_widget(self, widget):
        self.set_state_recursive(widget, ['!disabled'])

    def set_state_recursive(self, widget, state):
        widget.state(state)
        for child_widget in widget.children.values():
            self.set_state_recursive(child_widget, state)

    def browse_for_file(self):
        new_filename = filedialog.askopenfilename(
            initialdir='D:\\video\\GoswamiMj-videos',
            filetypes=[('mp4 or mp3', '*.mp4;*.mp3')]
        )
        if new_filename:
            self.filename.set(new_filename)
            self.load_metadata(new_filename)

    def load_metadata(self, source_filename):
        self.lang.set(meta.get_lang(source_filename))
        self.enable_widget(self.lang_frame)

    def lang_changed_callback(self):
        new_lang = self.lang.get()
        old_lang = meta.get_lang(self.filename.get())
        if new_lang != old_lang:
            meta.update_yaml(self.filename.get(), 'lang', new_lang)

root = tk.Tk()
root.title('Best Talks\' Uploader')
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

file_frame = FileFrame(mainframe)
file_frame.frame.grid(column=0, row=0)

root.mainloop()
