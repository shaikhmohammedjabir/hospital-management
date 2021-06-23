
from tkinter import Tk

class Admin(Tk):
    def __init__(self):
        super().__init__()
        self.title("admin site")
        self.geometry("{}x{}".format(self.winfo_screenwidth(),self.winfo_screenheight()))


