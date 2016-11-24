import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import re

import meta


class FileFrame():
    frame = None
    filename = None
    lang = None
    lang_frame = None
    title_rus = None
    title_rus_entry = None
    title_eng = None
    title_eng_entry = None
    descr_rus = None
    descr_rus_widget = None

    def __init__(self, parent_frame):
        self.frame = ttk.LabelFrame(parent_frame, text='Source file: ')
        ttk.Label(self.frame, text="File name:").grid(column=0, row=0, sticky=tk.W)

        self.filename = tk.StringVar()
        self.filename.set('(not selected)')
        filename_entry = ttk.Entry(self.frame, width=60, textvariable=self.filename)
        filename_entry.configure(state='readonly')
        filename_entry.grid(column=1, row=0, sticky='nwse')

        ttk.Button(self.frame, text='Browse...', command=self.browse_for_file).grid(column=2, row=0, sticky='nw')

        self.lang = tk.StringVar()
        self.lang.set('en')
        self.lang.trace('w', lambda *args: self.lang_changed_callback())
        self.lang_frame = ttk.LabelFrame(self.frame, text='Source language:')
        ttk.Radiobutton(self.lang_frame, text='English', variable=self.lang, value='en').grid()
        ttk.Radiobutton(self.lang_frame, text='Russian', variable=self.lang, value='ru').grid()
        self.lang_frame.grid(column=0, row=1, columnspan=3, sticky='nw')
        self.disable_widget(self.lang_frame)

        self.title_rus = tk.StringVar()
        self.title_rus.trace('w', lambda *args: self.title_rus_changed_callback())
        ttk.Label(self.frame, text="Title (Rus):").grid(row=2, column=0, sticky='nw')
        self.title_rus_entry = ttk.Entry(self.frame, state=['disabled'], textvariable=self.title_rus, width=70)
        self.title_rus_entry.grid(row=2, column=1, columnspan=2, sticky='nwse')

        self.title_eng = tk.StringVar()
        self.title_eng.trace('w', lambda *args: self.title_eng_changed_callback())
        ttk.Label(self.frame, text="Title (Eng):").grid(row=3, column=0, sticky='nw')
        self.title_eng_entry = ttk.Entry(self.frame, state=['disabled'], textvariable=self.title_eng, width=70)
        self.title_eng_entry.grid(row=3, column=1, columnspan=2, sticky='nwse')

        self.descr_rus = ''
        ttk.Label(self.frame, text='Descr (Rus):').grid(row=4, column=0, sticky='nw')
        self.descr_rus_widget = tk.Text(self.frame, state='disabled', width=70, height=7, undo=True, font='TkTextFont')
        self.descr_rus_widget.grid(row=4, column=1, columnspan=2, sticky='nwse')

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
            filetypes=[('Supported files (mp4, mp3, sesx)', '*.mp4;*.mp3;*.sesx')]
        )
        if new_filename:
            new_filename = re.sub(r' ru\.sesx$', '.mp4', new_filename)
            self.filename.set(new_filename)
            self.load_metadata(new_filename)

    def load_metadata(self, source_filename):
        self.lang.set(meta.get_lang(source_filename))
        self.enable_widget(self.lang_frame)

        self.title_rus.set(meta.get_title_ru(source_filename))
        self.enable_widget(self.title_rus_entry)

        self.title_eng.set(meta.get_title_en(source_filename))
        self.enable_widget(self.title_eng_entry)

        self.descr_rus_widget.delete('1.0', tk.END)
        self.descr_rus_widget.configure(state='normal')
        descr = meta.get_description_ru(source_filename).strip()
        self.descr_rus_widget.insert('1.0', descr)
        self.descr_rus_widget.edit_modified(False)
        self.descr_rus_widget.bind('<<Modified>>', self.descr_rus_modified)

    def descr_rus_modified(self, *args):
        really_modified = self.descr_rus_widget.edit_modified()
        if not really_modified:
            return
        text = self.descr_rus_widget.get('1.0', tk.END).strip()
        meta.update_yaml(self.filename.get(), 'descr_rus', text)
        self.descr_rus_widget.edit_modified(False)

    def lang_changed_callback(self):
        new_lang = self.lang.get()
        old_lang = meta.get_lang(self.filename.get())
        if new_lang != old_lang:
            meta.update_yaml(self.filename.get(), 'lang', new_lang)

    def title_rus_changed_callback(self):
        meta.update_yaml(self.filename.get(), 'title_rus', self.title_rus.get())

    def title_eng_changed_callback(self):
        meta.update_yaml(self.filename.get(), 'title_eng', self.title_eng.get())


root = tk.Tk()
root.title('Best Talks\' Uploader')
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

file_frame = FileFrame(mainframe)
file_frame.frame.grid(column=0, row=0)

root.mainloop()
