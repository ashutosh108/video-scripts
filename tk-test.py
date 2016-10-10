#!/usr/bin/env python
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky=tk.N+tk.E+tk.S+tk.W)
        self.createWidgets()

    def createWidgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.quitButton = tk.Button(self, text='Quit',
            command=self.quit)
        self.quitButton.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)

app = Application()
app.master.title('Sample application')
app.mainloop()