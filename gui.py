import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


def calculate(*args):
    try:
        value = float(feet.get())
        meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass


class FileFrame():
    frame = None
    filename = None
    lang = None

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
        lang_frame = ttk.LabelFrame(self.frame, text='Source language:')
        ttk.Radiobutton(lang_frame, text='English', variable=self.lang, value='en').grid()
        ttk.Radiobutton(lang_frame, text='Russian', variable=self.lang, value='ru').grid()
        lang_frame.grid()

    def browse_for_file(self):
        new_filename = filedialog.askopenfilename(
            initialdir='D:\\video\\GoswamiMj-videos',
            filetypes=[('mp4 or mp3', '*.mp4;*.mp3')]
        )
        if new_filename:
            self.filename.set(new_filename)

root = tk.Tk()
root.title('Best Talks\' Uploader')
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

file_frame = FileFrame(mainframe)
file_frame.frame.grid(column=0, row=0)

feet = tk.StringVar()
meters = tk.StringVar()
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(tk.W, tk.E))
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=tk.W)
ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=tk.W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=tk.E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=tk.W)
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
feet_entry.focus()
root.bind('<Return>', calculate)
root.mainloop()