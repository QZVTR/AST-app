import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import *

LARGEFONT = ("Verdana", 35)

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Page1, Page2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont, text=None, file_contents=None):
        frame = self.frames[cont]
        if text is not None:
            frame.update_text(text)
        if file_contents is not None:
            frame.display_file_contents(file_contents)
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label(self, text="Startpage", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_frame(Page1))
        button1.grid(row=1, column=1, padx=10, pady=10)

        
        self.entry_var = tk.StringVar()  # Variable to store user input
        entry = Entry(self, width=40, textvariable=self.entry_var)  # Entry widget to get user input
        entry.focus_set()
        entry.grid(row=3, column=1, padx=10, pady=10)

class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label(self, text="Page 1", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="StartPage",
                             command=lambda: controller.show_frame(StartPage))
        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Page 2",
                             command=lambda: controller.show_frame(Page2, controller.frames[StartPage].entry_var.get()))
        button2.grid(row=2, column=1, padx=10, pady=10)

        button3 = ttk.Button(self, text="Select File",
                             command=lambda: self.load_file(controller))
        button3.grid(row=3, column=1, padx=10, pady=10)

    def load_file(self, controller):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            with open(file_path, 'r') as file:
                file_contents = file.read()
            controller.show_frame(Page2, file_contents=file_contents)

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.label = ttk.Label(self, text="Page 2", font=LARGEFONT)
        self.label.grid(row=0, column=4, padx=10, pady=10)
        
        self.text_area = Text(self, height=10, width=50)
        self.text_area.grid(row=1, column=1, padx=10, pady=10)

    def display_file_contents(self, contents):
        self.text_area.delete(1.0, END)
        self.text_area.insert(1.0, contents)



app = tkinterApp()
app.mainloop()