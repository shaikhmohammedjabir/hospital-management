
from tkinter import Tk,Frame,Label,Button,PhotoImage

class Admin(Tk):
    def __init__(self):
        super().__init__()
        self.title("admin site")
        self.geometry("{}x{}".format(self.winfo_screenwidth(),self.winfo_screenheight()))

        left_frame=Frame(self,bd=1)
        right_frame=Frame(self)
        left_frame.pack(fill='y',side='left')
        right_frame.pack(fill='y',side='left')

        Label(left_frame,text="hellow").pack()
        Label(right_frame,text="hellow").pack()
        img=PhotoImage(file='icon/doctor.png')
        doctor=Button(left_frame,image=img)
        doctor.pack()


        self.mainloop()

#Admin()