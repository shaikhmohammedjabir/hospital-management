
from tkinter import Tk,Label,Button,Frame
from PIL import Image,ImageTk

class Appointment(Tk):
    def __init__(self):
        super().__init__()
        self.title("appointment desk")
        self.geometry("800x528")

        center_frame=Frame(self)
        center_frame.pack(pady=180)
        search_img=ImageTk.PhotoImage(image=Image.open('icon/search_appointment.png').resize((100,100)))
        search_btn=Button(center_frame,image=search_img,relief='solid')
        search_btn.grid(row=0,column=0,padx=10)

        add_img=ImageTk.PhotoImage(image=Image.open('icon/add_appointment.png').resize((100,100)))
        add_btn=Button(center_frame,image=add_img,relief='solid')
        add_btn.grid(row=0,column=1)

        self.mainloop()

Appointment()