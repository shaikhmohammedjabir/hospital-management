
from tkinter import Tk,Label,Button,Entry,OptionMenu,IntVar,StringVar,Frame
from tkinter.messagebox import showwarning,showinfo
from tkinter.ttk import Treeview
from time import strftime,localtime
from sqlite3 import connect,OperationalError
from PIL import Image,ImageTk
from sys import stderr


class Doctor(Tk):
    def __init__(self):
        super().__init__()
        self.title("doctor site")
        self.geometry("900x528")
        self.resizable(False, False)
        left_frame=Frame(self,bd=1)
        right_frame=Frame(self)
        left_frame.pack(fill='y',side='left')
        right_frame.pack(fill='y',side='left')
        doctor_add_img = ImageTk.PhotoImage(image=Image.open('icon/add.png').resize((100, 100)))
        doctor_add = Button(left_frame, image=doctor_add_img, relief='solid')
        doctor_add.pack()
        doctor_add.bind('<Return>', lambda event: self._Doctor__addDoctor(right_frame))
        doctor_add.bind('<KP_Enter>', lambda event: self._Doctor__addDoctor(right_frame))
        doctor_add.bind('<space>', lambda event: self._Doctor__addDoctor(right_frame))
        doctor_add.bind('<Button-1>', lambda event: self._Doctor__addDoctor(right_frame))
        doctor_add.bind('<Button-3>', lambda event: self._Doctor__addDoctor(right_frame))
        # update button
        patient_img = ImageTk.PhotoImage(Image.open('icon/patient.png').resize((100, 100)))
        patient_btn = Button(left_frame, image=patient_img, relief='solid')
        patient_btn.pack()
        patient_btn.bind('<Return>', lambda event: self._Doctor__patientList(right_frame))
        patient_btn.bind('<KP_Enter>', lambda event: self._Doctor__patientList(right_frame))
        patient_btn.bind('<space>', lambda event: self._Doctor__patientList(right_frame))
        patient_btn.bind('<Button-1>', lambda event: self._Doctor__patientList(right_frame))
        patient_btn.bind('<Button-3>', lambda event: self._Doctor__patientList(right_frame))
        #mainloop
        self.mainloop()

    def __addDoctor(self,frame):
        self._Doctor__clearFrame(frame)
        Frame(frame,height=150).grid(row=0,column=0)
        # doctor name
        Label(frame, text='name').grid(row=1, column=0,padx=100)
        doctor_name = Entry(frame,bg='white')
        doctor_name.grid(row=1, column=1)
        # specialized in
        Label(frame, text="specialized in").grid(row=2, column=0)
        doctor_specialized = Entry(frame,bg='white')
        doctor_specialized.grid(row=2, column=1)
        # timing shift
        Label(frame, text="timing ").grid(row=3, column=0)
        hour = IntVar()
        hour.set(12)
        minute = IntVar()
        minute.set(15)
        shift = StringVar()
        shift.set('PM')
        OptionMenu(frame, hour, *[x for x in range(1, 13)]).grid(row=3, column=1,sticky='e')
        OptionMenu(frame, minute, *[x for x in range(1, 61)]).grid(row=3, column=2,sticky='w')
        OptionMenu(frame, shift, *['AM', 'PM']).grid(row=3, column=3)
        #submit button
        submit_btn=Button(frame,text='submit')
        submit_btn.grid(row=4,column=3)
        submit_btn.bind('<Return>', lambda event: database._Database__addDoctor(self,frame,doctor_name,doctor_specialized,hour,minute,shift))
        submit_btn.bind('<KP_Enter>', lambda event: database._Database__addDoctor(self,frame,doctor_name,doctor_specialized,hour,minute,shift))
        submit_btn.bind('<space>', lambda event: database._Database__addDoctor(self,frame,doctor_name,doctor_specialized,hour,minute,shift))
        submit_btn.bind('<Button-1>', lambda event: database._Database__addDoctor(self,frame,doctor_name,doctor_specialized,hour,minute,shift))
        submit_btn.bind('<Button-3>', lambda event: database._Database__addDoctor(doctor_name,doctor_specialized,hour,minute,shift))

    def __patientList(self,frame):
        self._Doctor__clearFrame(frame)
        try:
            cols=('first_visit', 'name', 'doctor_name', 'specialist_on','appointment_date')
        except IndexError as ie:
            stderr.write(str(ie) + '\n')
        else:
            table = Treeview(frame, columns=cols, show='headings',height=25)
            for value, size in zip(cols, [70, 180, 180,180,180]):
                table.column(value, width=size)
                table.heading(value, text=value)
            table.grid(row=0, column=0)
            appointee = database._Database__getUser()
            if appointee:
                for patient in appointee:
                    if strftime("%d-%B-%Y",localtime())==patient[-1].split()[-1]:
                        table.insert('','end',values=patient)
                return
            showinfo("patient","no patient for today")

    def __clearFrame(self, frame):
        frame_child = frame.winfo_children()
        if frame_child:
            for child in frame_child:
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
                sql = f"select first_time_visit,name,doctor_name,specialist_on,appointment_date from appointment"
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


database=Doctor.Database()