
from tkinter import Tk,Label,Button,Frame,Entry,Radiobutton,BooleanVar,ttk,IntVar
from sqlite3 import connect,OperationalError
from time import strftime,localtime
from PIL import Image,ImageTk
from re import compile,search

class Appointment(Tk):
    def __init__(self):
        super().__init__()
        self.title("appointment desk")
        self.geometry("800x528")

        left_frame = Frame(self)
        left_frame.pack(side='left',fill='y')
        right_frame=Frame(self)
        right_frame.pack(fill='both')
        #search appointment
        search_img = ImageTk.PhotoImage(image=Image.open('icon/search_appointment.png').resize((100, 100)))
        search_btn = Button(left_frame, image=search_img, relief='solid')
        search_btn.grid(row=0, column=0)
        search_btn.bind('<Return>', lambda event: self._Appointment__searchPatient(right_frame))
        search_btn.bind('<KP_Enter>', lambda event: self._Appointment__searchPatient(right_frame))
        search_btn.bind('<space>', lambda event: self._Appointment__searchPatient(right_frame))
        search_btn.bind('<Button-1>', lambda event: self._Appointment__searchPatient(right_frame))
        search_btn.bind('<Button-3>', lambda event: self._Appointment__searchPatient(right_frame))
        #add appointment
        add_img = ImageTk.PhotoImage(image=Image.open('icon/add_appointment.png').resize((100, 100)))
        add_btn = Button(left_frame, image=add_img, relief='solid')
        add_btn.grid(row=1, column=0)
        add_btn.bind('<Return>', lambda event: self._Appointment__addPatient(right_frame))
        add_btn.bind('<KP_Enter>', lambda event: self._Appointment__addPatient(right_frame))
        add_btn.bind('<space>', lambda event: self._Appointment__addPatient(right_frame))
        add_btn.bind('<Button-1>', lambda event: self._Appointment__addPatient(right_frame))
        add_btn.bind('<Button-3>', lambda event: self._Appointment__addPatient(right_frame))

        self.mainloop()

    def __searchPatient(self,frame):
        self._Appointment__clearFrame(frame)

    def __addPatient(self,frame):
        __month={'January':31,
                 'February':28,
                 'March':31,
                 'April':30,
                 'May':31,
                 'June':30,
                 'July':31,
                 'August':31,
                 'September':30,
                 'October':31,
                 'November':30,
                 'December':31}
        self._Appointment__clearFrame(frame)
        #header
        Label(frame,text="Request an Appointment\n\n",fg='green',font=',16,').grid(row=0,column=0)
        # visit
        flag = BooleanVar()
        Label(frame, text="First Time Visit?").grid(row=1, column=0)
        Radiobutton(frame, text='Yes',value=True, variable=flag).grid(row=2, column=1,sticky='w')
        Radiobutton(frame, text='No',value=False, variable=flag).grid(row=3, column=1,sticky='w')
        #name
        Label(frame,text='Name').grid(row=4,column=0)
        name_field=Entry(frame,bg='white')
        name_field.grid(row=4,column=1)
        #phone
        Label(frame,text="Phone Number").grid(row=5,column=0)
        phone_field=Entry(frame,bg='white')
        phone_field.grid(row=5,column=1)
        #email
        Label(frame,text="E-mail").grid(row=6,column=0)
        email_field=Entry(frame,bg='white')
        email_field.grid(row=6,column=1)
        email_field.bind('<FocusOut>',lambda x:self._Appointment__validateForm(frame,email_field,submit_btn))
        #appointment date
        date_var=IntVar()
        month,year=strftime("%B %Y", localtime()).split(' ')
        ttk.LabeledScale(frame,variable=date_var,from_=1,to=__month[month]).grid(row=7,column=1)
        Label(frame,text=month.upper()+' '+year,font=',14,').grid(row=7,column=2)
        #submit button
        submit_btn=Button(frame,text="get appointment")
        submit_btn.grid(row=10,column=2)
        submit_btn.bind('<Return>', lambda event: self._Appointment__insertPatient(flag,name_field,phone_field,email_field,date_var,month,year))
        submit_btn.bind('<KP_Enter>', lambda event: self._Appointment__insertPatient(flag,name_field,phone_field,email_field,date_var,month,year))
        submit_btn.bind('<space>', lambda event: self._Appointment__insertPatient(flag,name_field,phone_field,email_field,date_var,month,year))
        submit_btn.bind('<Button-1>', lambda event: self._Appointment__insertPatient(flag,name_field,phone_field,email_field,date_var,month,year))
        submit_btn.bind('<Button-3>', lambda event: self._Appointment__insertPatient(flag,name_field,phone_field,email_field,date_var,month,year))

        #existance check for existing user
        #self.bind('<Return>',lambda x:print(flag.get()))
        #first_time_visit , name, phone, email         appointment_date

    def __insertPatient(self):
        pass

    def __validateForm(self,frame,field,submit_btn):
        if search(compile("[A-Za-z0-9_]+@[A-Za-z]+.[A-Za-z]{2,3}"),field.get()):
            field.configure(bg='green')
            submit_btn.configure(state='active')
        else:
            field.configure(bg='red')
            submit_btn.configure(state='disabled')

    def __clearFrame(self,frame):
        for child in frame.winfo_children():
            child.destroy()

    class Database:
        def __init__(self):
            self.database=connect('database/hospital.db')
            self.cursor=self.database.cursor()

        def __getHeader(self,*,table_name):
            self.cursor.execute(f"pragma table_info('{table_name}')")
            return self.cursor.fetchall()

        def __getUser(self):
            try:
                sql = f"select * from appointment"
                self.cursor.execute(sql)
                return self.cursor.fetchall()
            except OperationalError as oe:
                stderr.write(str(oe) + '\n')
                return None

        def __addDoctor(self,main_app,frame,doctor_name, doctor_specialized, hour, minute, shift):
            doctor_name=doctor_name.get()
            doctor_specialized=doctor_specialized.get()
            shift=f"{hour.get()}:{minute.get()} {shift.get()}"
            try:
                if doctor_name:
                    self.cursor.execute(f"insert into doctor(name,specialize_in,timing) values('{doctor_name}','{doctor_specialized}','{shift}')")
                    self.database.commit()
                    main_app._Doctor__addDoctor(frame)
                    showinfo("success","you added successfully in database")
                else:
                    showwarning('doctorname',"enter name first")
            except OperationalError as oe:
                stderr.write(str(oe)+'\n')

        def __del__(self):
            self.cursor.close()
            self.database.close()

database=Appointment.Database()
Appointment()