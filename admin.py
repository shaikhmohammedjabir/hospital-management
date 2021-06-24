
from tkinter import Tk,Frame,Label,Button,PhotoImage
from PIL import Image,ImageTk

class Admin(Tk):
    def __init__(self):
        super().__init__()
        self.title("admin site")
        self.geometry("800x528")

        left_frame=Frame(self,bd=1)
        right_frame=Frame(self)
        left_frame.pack(fill='y',side='left')
        right_frame.pack(fill='y',side='left')

        user_add=ImageTk.PhotoImage(image=Image.open('icon/add.png').resize((100, 100)))
        user_btn=Button(left_frame,image=user_add,activebackground='green')
        user_btn.pack()

        update_img = ImageTk.PhotoImage(Image.open('icon/update.png').resize((100, 100)))
        update_btn = Button(left_frame, image=update_img,activebackground='green')
        update_btn.pack()

        patient_img = ImageTk.PhotoImage(Image.open('icon/patient.png').resize((100, 100)))
        patient_btn = Button(left_frame, image=patient_img,activebackground='green')
        patient_btn.pack()

        appointment_img = ImageTk.PhotoImage(Image.open('icon/appointment.png').resize((100, 100)))
        appointment_btn = Button(left_frame, image=appointment_img,activebackground='green')
        appointment_btn.pack()

        doctor_img = ImageTk.PhotoImage(Image.open('icon/doctor.png').resize((100, 100)))
        doctor_btn = Button(left_frame, image=doctor_img,activebackground='green')
        doctor_btn.pack()

        self.mainloop()

Admin()