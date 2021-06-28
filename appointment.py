
from tkinter import Tk,Label,Button,Frame,Entry,Radiobutton,StringVar,ttk,IntVar
from tkinter.messagebox import showinfo,showwarning
from sqlite3 import connect,OperationalError
from time import strftime,localtime
from PIL import Image,ImageTk
from re import compile,search
from sys import stderr

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
        Label(frame,text="get appointment details\n\n",fg='green',font=',16,').grid(row=0,column=0,padx=10)
        entry=Entry(frame,bg='white')
        entry.grid(row=1,column=0)
        btn=Button(frame,text='search',relief='solid')
        btn.grid(row=1,column=1)
        btn.bind('<Return>', lambda event: self._Appointment__getPatientData(frame,entry))
        btn.bind('<KP_Enter>', lambda event: self._Appointment__getPatientData(frame,entry))
        btn.bind('<space>', lambda event: self._Appointment__getPatientData(frame,entry))
        btn.bind('<Button-1>', lambda event: self._Appointment__getPatientData(frame,entry))
        btn.bind('<Button-3>', lambda event: self._Appointment__getPatientData(frame,entry))

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
        flag = StringVar()
        flag.set(' ')
        Label(frame, text="First Time Visit?").grid(row=1, column=0)
        Radiobutton(frame, text='Yes',value='yes', variable=flag).grid(row=2, column=1,sticky='w')
        Radiobutton(frame, text='No',value='no', variable=flag).grid(row=3, column=1,sticky='w')
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
        Label(frame,text="date").grid(row=7,column=0)
        date_var=IntVar()
        month,year=strftime("%B %Y", localtime()).split(' ')
        ttk.LabeledScale(frame,variable=date_var,from_=1,to=__month[month]).grid(row=7,column=1)
        Label(frame,text=month.upper()+' '+year,font=',14,').grid(row=7,column=2)
        #doctor details
        doc_frame = Frame(frame)
        doc_frame.grid(row=10, column=0, columnspan=3)
        cols = [*zip(*database._Database__getHeader(table_name='doctor'))][1]
        tree = ttk.Treeview(doc_frame, columns=cols, show='headings')
        for value, size in zip(cols, [40, 250, 200, 150]):
            tree.column(value, width=size)
            tree.heading(value, text=value)
        for doctor in database._Database__getDoctorDetails():
            tree.insert('', 'end', values=doctor)
        tree.grid(row=0, column=0)
        #submit button
        submit_btn=Button(frame,text="get appointment")
        submit_btn.grid(row=11,column=2)
        submit_btn.bind('<Return>', lambda event: self._Appointment__insertPatientData(self,frame,flag.get(),name_field.get(),phone_field.get(),email_field.get(),date_var.get(),month,year,tree))
        submit_btn.bind('<KP_Enter>', lambda event: self._Appointment__insertPatientData(self,frame,flag.get(),name_field.get(),phone_field.get(),email_field.get(),date_var.get(),month,year,tree))
        submit_btn.bind('<space>', lambda event: self._Appointment__insertPatientData(self,frame,flag.get(),name_field.get(),phone_field.get(),email_field.get(),date_var.get(),month,year,tree))
        submit_btn.bind('<Button-1>', lambda event: self._Appointment__insertPatientData(self,frame,flag.get(),name_field.get(),phone_field.get(),email_field.get(),date_var.get(),month,year,tree))
        submit_btn.bind('<Button-3>', lambda event: self._Appointment__insertPatientData(self,frame,flag.get(),name_field.get(),phone_field.get(),email_field.get(),date_var.get(),month,year,tree))

    def __insertPatientData(self,main_app,frame,flag,name_field,phone_field,email_field,date_var,month,year,tree):
        try:
            doctor_name,specialist_on,time=tree.item(tree.selection())['values'][1:]
        except ValueError as ve:
            showwarning("fill-up",str(ve))
        try:
            database._Database__addAppointment(main_app,frame,flag,name_field,phone_field,email_field,f"{time} {date_var}-{month}-{year}",doctor_name,specialist_on)
        except UnboundLocalError:
            showwarning("doctor","doctors are unavailable")

    def __getPatientData(self,frame,entry):
        inner_frame=Frame(frame,bg)
        inner_frame.grid(row=2,column=0,columnspan=2)
        entry=entry.get()
        patient_table=database._Database__getAppointmentDetails(patient_name=entry)
        cols=('name','doctor_name','specialist_on','appointment_date')
        tree=ttk.Treeview(inner_frame,columns=cols,show='headings',height=20)
        for value,size in zip(cols,[180,180,150,180]):
            tree.heading(value,text=value)
            tree.column(value,width=size)
        tree.pack(fill='x',side='left')
        if patient_table:
            for patient in patient_table:
                tree.insert('','end',values=patient)
            return
        showwarning("appointment","no appointment available for "+entry)

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

        def __getDoctorDetails(self):
            try:
                sql = f"select * from doctor"
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

        def __addAppointment(self,main_app,frame,flag,name_field,phone_field,email_field,apointment_date,doctor_name,specialist_on):
            try:
                if doctor_name:
                    self.cursor.execute(f"insert into appointment(first_time_visit,name,phone ,email,appointment_date,doctor_name,specialist_on) values('{flag}','{name_field}','{phone_field}','{email_field}','{apointment_date}','{doctor_name}','{specialist_on}')")
                    self.database.commit()
                    main_app._Appointment__addPatient(frame)
                    showinfo("success","you added successfully in database")
                else:
                    showwarning('doctorname',"enter name first")
            except OperationalError as oe:
                stderr.write(str(oe)+'\n')

        def __getAppointmentDetails(self,*,patient_name):
            try:
                sql = f"select name,doctor_name,specialist_on,appointment_date from appointment where name='{patient_name}'"
                self.cursor.execute(sql)
                return self.cursor.fetchall()
            except OperationalError as oe:
                stderr.write(str(oe) + '\n')
                return None


        def __del__(self):
            self.cursor.close()
            self.database.close()

database=Appointment.Database()