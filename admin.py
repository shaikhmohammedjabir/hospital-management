
from tkinter import Tk,Frame,Label,Button,Entry,OptionMenu,StringVar
from tkinter.messagebox import showwarning
from tkinter.ttk import Treeview
from sqlite3 import connect,OperationalError
from PIL import Image,ImageTk
from hashlib import sha3_512
from sys import stderr

class Admin(Tk):
    def __init__(self):
        super().__init__()
        self.title("admin site")
        self.geometry("800x528")
        self.resizable(False,False)
        global member

        left_frame=Frame(self,bd=1)
        right_frame=Frame(self)
        left_frame.pack(fill='y',side='left')
        right_frame.pack(fill='y',side='left')
        #member button
        member_add=ImageTk.PhotoImage(image=Image.open('icon/add.png').resize((100, 100)))
        member_btn=Button(left_frame,image=member_add,relief='solid')
        member_btn.pack()
        member_btn.bind('<Return>',lambda event:member._Member__createMember(right_frame))
        member_btn.bind('<KP_Enter>',lambda event:member._Member__createMember(right_frame))
        member_btn.bind('<space>',lambda event:member._Member__createMember(right_frame))
        member_btn.bind('<Button-1>',lambda event:member._Member__createMember(right_frame))
        member_btn.bind('<Button-3>',lambda event:member._Member__createMember(right_frame))
        #update button
        update_img = ImageTk.PhotoImage(Image.open('icon/update.png').resize((100, 100)))
        update_btn = Button(left_frame, image=update_img,relief='solid')
        update_btn.pack()
        update_btn.bind('<Return>', lambda event: member._Member__updateMember(right_frame))
        update_btn.bind('<KP_Enter>', lambda event: member._Member__updateMember(right_frame))
        update_btn.bind('<space>', lambda event: member._Member__updateMember(right_frame))
        update_btn.bind('<Button-1>', lambda event: member._Member__updateMember(right_frame))
        update_btn.bind('<Button-3>', lambda event: member._Member__updateMember(right_frame))
        #patient button
        patient_img = ImageTk.PhotoImage(Image.open('icon/patient.png').resize((100, 100)))
        patient_btn = Button(left_frame, image=patient_img,relief='solid')
        patient_btn.pack()
        #appointment button
        appointment_img = ImageTk.PhotoImage(Image.open('icon/appointment.png').resize((100, 100)))
        appointment_btn = Button(left_frame, image=appointment_img,relief='solid')
        appointment_btn.pack()
        #doctor button
        doctor_img = ImageTk.PhotoImage(Image.open('icon/doctor.png').resize((100, 100)))
        doctor_btn = Button(left_frame, image=doctor_img,relief='solid')
        doctor_btn.pack()

        self.mainloop()


    class Member:
        def __createMember(self,frame):
            self._Member__clearFrame(frame)
            Frame(frame,height=150).grid(row=0,column=0)
            Label(frame,text='membername',font=',13,').grid(row=1,column=0,padx=60)
            member_entry=Entry(frame)
            member_entry.grid(row=1,column=1)
            member_entry.focus_set()
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
            create_btn.bind('<Return>',lambda x:self._Member__validateMember(member_entry,password_entry,default_value))
            create_btn.bind('<KP_Enter>',lambda x:self._Member__validateMember(member_entry,password_entry,default_value))
            create_btn.bind('<space>',lambda x:self._Member__validateMember(member_entry,password_entry,default_value))
            create_btn.bind('<Button-1>', lambda x: self._Member__validateMember(member_entry, password_entry, default_value))
            create_btn.bind('<Button-3>', lambda x: self._Member__validateMember(member_entry, password_entry, default_value))

        def __updateMember(self,frame):
            #print(database._Database__get(role='doctor'))
            self._Member__clearFrame(frame)
            try:
                cols=list(zip(*database._Database__getHeader(table_name='user')))[1]
            except IndexError as ie:
                stderr.write(str(ie)+'\n')
            else:
                default_value = StringVar()
                default_value.set('all')
                table=Treeview(frame,columns=cols,show='headings',height=20)
                for value,size in zip(cols,[50,240,300,100]):
                    table.column(value,width=size)
                    table.heading(value,text=value)
                self._Member__updateTable(table, default_value)
                table.grid(row=0,column=0)
            down_frame=Frame(frame)
            down_frame.grid(row=1,column=0)
            OptionMenu(down_frame,default_value,*('all','appointment','doctor')).grid(row=0,column=0)
            #get button
            get_button=Button(down_frame,text='get')
            get_button.bind('<Return>',lambda x:self._Member__updateTable(table,default_value))
            get_button.bind('<KP_Enter>',lambda x:self._Member__updateTable(table,default_value))
            get_button.bind('<space>',lambda x:self._Member__updateTable(table,default_value))
            get_button.bind('<Button-1>', lambda x:self._Member__updateTable(table,default_value))
            get_button.bind('<Button-3>', lambda x:self._Member__updateTable(table,default_value))
            get_button.grid(row=0, column=1)
            #delete button
            delete_button = Button(down_frame, text='delete')
            delete_button.bind('<Return>', lambda x: self._Member__deleteMember(frame,table,default_value))
            delete_button.bind('<KP_Enter>', lambda x: self._Member__deleteMember(frame,table,default_value))
            delete_button.bind('<space>', lambda x: self._Member__deleteMember(frame,table,default_value))
            delete_button.bind('<Button-1>', lambda x: self._Member__deleteMember(frame,table,default_value))
            delete_button.bind('<Button-3>', lambda x: self._Member__deleteMember(frame,table,default_value))
            delete_button.grid(row=0, column=2)

        def __deleteMember(self,frame,table,default_value):
            for user in table.selection():
                database._Database__delete(table.item(user,'values')[0])
                self._Member__updateTable(table, default_value)

        def __validateMember(self,member_name,password,role):
            global database
            member_name=member_name.get()
            password=sha3_512(bytes(password.get(),encoding='utf-8',errors='strict')).hexdigest()
            role=role.get()
            #member existance check
            if database._Database__enquiry(member_name):
                showwarning('member',"member already exists use unique name")
                return
            database._Database__insert(member_name,password,role)

        def __clearFrame(self,frame):
            frame_child=frame.winfo_children()
            if frame_child:
                for child in frame_child:
                    child.destroy()

        def __updateTable(self,table,default_value):
            for item in table.get_children():
                table.delete(item)
            role = default_value.get()
            if role == 'all':
                role = '*'
            for value in database._Database__getUser(role=role):
                table.insert('', 'end', values=value)

    class Database:
        def __init__(self):
            self.database=connect('database/hospital.db')
            self.cursor=self.database.cursor()

        def __enquiry(self,member_name):
            try:
                self.cursor.execute(f"select user_name from user where user_name='{member_name}'")
                result=self.cursor.fetchone()
                if result:
                    return True
            except OperationalError as oe:
                stderr.write(str(oe)+'\n')
            return False

        def __insert(self,member_name,password,role):
            try:
                if member_name:
                    self.cursor.execute(f"insert into user(user_name,password,role) values('{member_name}','{password}','{role}')")
                    self.database.commit()
                else:
                    showwarning('membername',"enter member name first")
            except OperationalError as oe:
                stderr.write(str(oe)+'\n')

        def __delete(self,member_sl):
            try:
                self.cursor.execute(f"delete from user where sl='{member_sl}'")
                self.database.commit()
            except OperationalError as oe:
                stderr.write(str(oe)+'\n')

        def __getUser(self,*,role='*'):
            try:
                sql = f"select * from user"
                if role!='*':
                    sql+=f" where role='{role}'"
                self.cursor.execute(sql)
                return self.cursor.fetchall()
            except OperationalError as oe:
                stderr.write(str(oe)+'\n')
                return None

        def __getHeader(self,*,table_name):
            self.cursor.execute(f"pragma table_info('{table_name}')")
            return self.cursor.fetchall()

        def __del__(self):
            self.cursor.close()
            self.database.close()


database=Admin.Database()
member=Admin.Member()
###testing code below delete when development complete
Admin()