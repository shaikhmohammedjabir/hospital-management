
from tkinter import Tk,Frame,Label,Button,Entry
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
        #user button
        user_add=ImageTk.PhotoImage(image=Image.open('icon/add.png').resize((100, 100)))
        user_btn=Button(left_frame,image=user_add,activebackground='green',relief='solid')
        user_btn.pack()
        user_btn.bind('<Return>',lambda event:self.User(right_frame))
        user_btn.bind('<KP_Enter>',lambda event:self.User(right_frame))
        user_btn.bind('<space>',lambda event:self.User(right_frame))
        user_btn.bind('<Button-1>',lambda event:self.User(right_frame))
        user_btn.bind('<Button-3>',lambda event:self.User(right_frame))
        #update button
        update_img = ImageTk.PhotoImage(Image.open('icon/update.png').resize((100, 100)))
        update_btn = Button(left_frame, image=update_img,activebackground='green',relief='solid')
        update_btn.pack()
        #patient button
        patient_img = ImageTk.PhotoImage(Image.open('icon/patient.png').resize((100, 100)))
        patient_btn = Button(left_frame, image=patient_img,activebackground='green',relief='solid')
        patient_btn.pack()
        #appointment button
        appointment_img = ImageTk.PhotoImage(Image.open('icon/appointment.png').resize((100, 100)))
        appointment_btn = Button(left_frame, image=appointment_img,activebackground='green',relief='solid')
        appointment_btn.pack()
        #doctor button
        doctor_img = ImageTk.PhotoImage(Image.open('icon/doctor.png').resize((100, 100)))
        doctor_btn = Button(left_frame, image=doctor_img,activebackground='green',relief='solid')
        doctor_btn.pack()

        self.mainloop()
    class User:
        def __init__(self,frame):
            Label(frame,text='username',font=',13,').grid(row=0,column=0,ipady=80,ipadx=20)
            user_entry=Entry(frame)
            user_entry.grid(row=0,column=1)
            Label(frame,text='password',font=',13,').grid(row=1,column=0)
            password_entry=Entry(frame,show='*')
            password_entry.grid(row=1,column=1)

Admin()