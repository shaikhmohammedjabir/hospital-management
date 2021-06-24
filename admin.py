
from tkinter import Tk,Frame,Label,Button,Entry,OptionMenu,StringVar
from tkinter.messagebox import showwarning
from sqlite3 import connect,OperationalError
from PIL import Image,ImageTk
from hashlib import sha3_512
from sys import stderr

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
            Frame(frame,height=150).grid(row=0,column=0)
            Label(frame,text='username',font=',13,').grid(row=1,column=0,padx=60)
            user_entry=Entry(frame)
            user_entry.grid(row=1,column=1)
            Label(frame,text='password',font=',13,').grid(row=2,column=0)
            password_entry=Entry(frame,show='*')
            password_entry.grid(row=2,column=1)
            Label(frame,text="role",font=',13,').grid(row=3,column=0)
            default_value=StringVar()
            default_value.set('appointment')
            role_value=OptionMenu(frame,default_value,*['appointment','doctor'])
            role_value.grid(row=3,column=1)
            create_btn=Button(frame,text='create',activebackground='green')
            create_btn.grid(row=4,column=1,sticky='e')
            create_btn.bind('<Return>',lambda x:self.createUser(user_entry,password_entry,default_value))
            create_btn.bind('<KP_Enter>',lambda x:self.createUser(user_entry,password_entry,default_value))
            create_btn.bind('<space>',lambda x:self.createUser(user_entry,password_entry,default_value))
            create_btn.bind('<Button-1>', lambda x: self.createUser(user_entry, password_entry, default_value))
            create_btn.bind('<Button-3>', lambda x: self.createUser(user_entry, password_entry, default_value))

        def createUser(self,user_name,password,role):
            user_name=user_name.get()
            password=sha3_512(bytes(password.get(),encoding='utf-8',errors='strict')).hexdigest()
            role=role.get()
            #user existance check
            db=Admin.Database()
            if db.userEnquiry(user_name):
                showwarning('user',"user already exists use unique name")
                return
            db.userInsert(user_name,password,role)

    class Database:
        def __init__(self):
            self.database=connect('database/hospital.db')
            self.cursor=self.database.cursor()

        def userEnquiry(self,user_name):
            try:
                self.cursor.execute(f"select user_name from user where user_name='{user_name}'")
                result=self.cursor.fetchone()
                if result:
                    return True
            except OperationalError as oe:
                stderr.write(str(oe)+'\n')
            return False

        def userInsert(self,user_name,password,role):
            try:
                self.cursor.execute(f"insert into user(user_name,password,role) values('{user_name}','{password}','{role}')")
                self.database.commit()
            except OperationalError as oe:
                stderr.write(str(oe)+'\n')

        def __del__(self):
            self.cursor.close()
            self.database.close()

Admin()