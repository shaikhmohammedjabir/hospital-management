
from tkinter import Tk,Frame,Label,Button,Entry,OptionMenu,StringVar
from tkinter.messagebox import showwarning,showinfo
from tkinter.ttk import Treeview
from sqlite3 import connect,OperationalError
from PIL import Image,ImageTk
from hashlib import sha3_512
from shutil import copy
from sys import stderr
from os import path,remove

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
        #database checking
        database_check_img = ImageTk.PhotoImage(Image.open('icon/database_checking.png').resize((100, 100)))
        database_check_btn = Button(left_frame, image=database_check_img,relief='solid')
        database_check_btn.pack()
        database_check_btn.bind('<Return>', lambda event: maintainance._Maintainance__checkDatabaseUser(right_frame))
        database_check_btn.bind('<KP_Enter>', lambda event: maintainance._Maintainance__checkDatabaseUser(right_frame))
        database_check_btn.bind('<space>', lambda event: maintainance._Maintainance__checkDatabaseUser(right_frame))
        database_check_btn.bind('<Button-1>', lambda event: maintainance._Maintainance__checkDatabaseUser(right_frame))
        database_check_btn.bind('<Button-3>', lambda event: maintainance._Maintainance__checkDatabaseUser(right_frame))
        #database maintainance
        database_maintain_img = ImageTk.PhotoImage(Image.open('icon/database_maintainance.png').resize((100, 100)))
        database_maintain_btn = Button(left_frame, image=database_maintain_img,relief='solid')
        database_maintain_btn.pack()
        database_maintain_btn.bind('<Return>', lambda event: maintainance._Maintainance__maintainDatabase(right_frame))
        database_maintain_btn.bind('<KP_Enter>', lambda event: maintainance._Maintainance__maintainDatabase(right_frame))
        database_maintain_btn.bind('<space>', lambda event: maintainance._Maintainance__maintainDatabase(right_frame))
        database_maintain_btn.bind('<Button-1>', lambda event: maintainance._Maintainance__maintainDatabase(right_frame))
        database_maintain_btn.bind('<Button-3>', lambda event: maintainance._Maintainance__maintainDatabase(right_frame))
        #doctor button
        exit_img = ImageTk.PhotoImage(Image.open('icon/logout_admin.png').resize((100, 100)))
        exit_btn = Button(left_frame, image=exit_img,relief='solid')
        exit_btn.pack()
        exit_btn.bind('<Return>', lambda event: exit("bye admin"))
        exit_btn.bind('<KP_Enter>', lambda event: exit("bye admin"))
        exit_btn.bind('<space>', lambda event: exit("bye admin"))
        exit_btn.bind('<Button-1>', lambda event: exit("bye admin"))
        exit_btn.bind('<Button-3>', lambda event: exit("bye admin"))

        self.mainloop()

    class Maintainance:
        def __init__(self):
            if not path.exists('database/hospital.db'):
                connect('database/hospital.db')

        def __checkDatabaseUser(self,frame):
            member._Member__clearFrame(frame)
            Label(frame,text="Check requirement and maintainance\n\n",fg='green',font=',16,').grid(row=0,column=0)
            check_user_btn=Button(frame,text="check tables",relief='solid')
            check_user_btn.grid(row=1,column=0)
            check_user_btn.bind('<Return>', lambda event: self._Maintainance__checkUser(frame,check_user_btn))
            check_user_btn.bind('<KP_Enter>', lambda event: self._Maintainance__checkUser(frame,check_user_btn))
            check_user_btn.bind('<space>', lambda event: self._Maintainance__checkUser(frame,check_user_btn))
            check_user_btn.bind('<Button-1>', lambda event: self._Maintainance__checkUser(frame,check_user_btn))
            check_user_btn.bind('<Button-3>', lambda event: self._Maintainance__checkUser(frame,check_user_btn))

        def __checkUser(self,frame,check_user_btn):
            frame_list=dict()
            user_list = database._Database__getTables()
            not_present_user=list(frozenset(['user', 'appointment', 'doctor']).difference(user_list))
            if not not_present_user:
                Label(frame, text="all tables are satisfied", fg='green').grid(row=1,column=2)
                return
            for index,user in enumerate(not_present_user):
                Label(frame,text=user,fg='red').grid(row=index+1,column=2)
            for children in frame.winfo_children():
                text=children['text']
                if text in not_present_user:
                    frame_list[text]=children
            #logic to check button condition and create undefined table
            if check_user_btn['text']=="create tables":
                if 'user' in not_present_user:
                    if database._Database__createUserTable():
                        frame_list['user'].configure(fg='green')
                if 'doctor' in not_present_user:
                    if database._Database__createDoctorTable():
                        frame_list['doctor'].configure(fg='green')
                if 'appointment' in not_present_user:
                    if database._Database__createAppointmentTable():
                        frame_list['appointment'].configure(fg='green')
            check_user_btn.configure(text="create tables")

        def __maintainDatabase(self,frame):
            member._Member__clearFrame(frame)
            Frame(frame,height=150).grid(row=0,column=0)
            create_label = Label(frame, text="action require?", fg='red')
            backup_label=Label(frame,text="action require?",fg='red')
            restore_label = Label(frame, text="action require?", fg='red')
            delete_label = Label(frame, text="action require?", fg='red')
            create_label.grid(row=1, column=1)
            backup_label.grid(row=2,column=1)
            restore_label.grid(row=3,column=1)
            delete_label.grid(row=4,column=1)
            create_btn=Button(frame,text="create",relief='solid',width=10)
            create_btn.grid(row=1, column=0, padx=100)
            create_btn.bind('<Return>', lambda event: self._Maintainance__createDatabase(create_label))
            create_btn.bind('<KP_Enter>', lambda event: self._Maintainance__createDatabase(create_label))
            create_btn.bind('<space>', lambda event: self._Maintainance__createDatabase(create_label))
            create_btn.bind('<Button-1>', lambda event: self._Maintainance__createDatabase(create_label))
            create_btn.bind('<Button-3>', lambda event: self._Maintainance__createDatabase(create_label))
            #create backup
            backup_btn=Button(frame,text="backup",relief='solid',width=10)
            backup_btn.grid(row=2,column=0,padx=100)
            backup_btn.bind('<Return>', lambda event: self._Maintainance__backupDatabase(backup_label))
            backup_btn.bind('<KP_Enter>', lambda event: self._Maintainance__backupDatabase(backup_label))
            backup_btn.bind('<space>', lambda event: self._Maintainance__backupDatabase(backup_label))
            backup_btn.bind('<Button-1>', lambda event: self._Maintainance__backupDatabase(backup_label))
            backup_btn.bind('<Button-3>', lambda event: self._Maintainance__backupDatabase(backup_label))
            #restore backup
            restore_btn=Button(frame, text="restore", relief='solid',width=10)
            restore_btn.grid(row=3,column=0)
            restore_btn.bind('<Return>', lambda event: self._Maintainance__restoreDatabase(restore_label))
            restore_btn.bind('<KP_Enter>', lambda event: self._Maintainance__restoreDatabase(restore_label))
            restore_btn.bind('<space>', lambda event: self._Maintainance__restoreDatabase(restore_label))
            restore_btn.bind('<Button-1>', lambda event: self._Maintainance__restoreDatabase(restore_label))
            restore_btn.bind('<Button-3>', lambda event: self._Maintainance__restoreDatabase(restore_label))
            #delete database
            delete_btn = Button(frame, text="delete", relief='solid',width=10)
            delete_btn.grid(row=4, column=0)
            delete_btn.bind('<Return>', lambda event: self._Maintainance__deleteDatabase(delete_label))
            delete_btn.bind('<KP_Enter>', lambda event: self._Maintainance__deleteDatabase(delete_label))
            delete_btn.bind('<space>', lambda event: self._Maintainance__deleteDatabase(delete_label))
            delete_btn.bind('<Button-1>', lambda event: self._Maintainance__deleteDatabase(delete_label))
            delete_btn.bind('<Button-3>', lambda event: self._Maintainance__deleteDatabase(delete_label))

        def __createDatabase(self,label):
            if not path.exists('database/hospital.db'):
                connect('database/hospital.db')
                label.config(text="task completed", fg='green')
                return
            label.config(text="database exists", fg='green')

        def __backupDatabase(self,label):
            if path.exists('database/hospital.db'):
                copy('database/hospital.db','database/hospital.db.backup')
                label.config(text="task completed",fg='green')

        def __restoreDatabase(self,label):
            try:
                remove('database/hospital.db')
            except FileNotFoundError as fnfe:
                stderr.write(str(fnfe)+'\n')
            if path.exists('database/hospital.db.backup'):
                copy('database/hospital.db.backup','database/hospital.db')
                label.config(text="task completed", fg='green')

        def __deleteDatabase(self,label):
            try:
                remove('database/hospital.db')
                label.config(text="task completed", fg='green')
            except FileNotFoundError:
                showwarning("file operation","no database to delete")

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
            create_btn.bind('<Return>',lambda x:self._Member__validateMember(frame,member_entry,password_entry,default_value))
            create_btn.bind('<KP_Enter>',lambda x:self._Member__validateMember(frame,member_entry,password_entry,default_value))
            create_btn.bind('<space>',lambda x:self._Member__validateMember(frame,member_entry,password_entry,default_value))
            create_btn.bind('<Button-1>', lambda x: self._Member__validateMember(frame,member_entry, password_entry, default_value))
            create_btn.bind('<Button-3>', lambda x: self._Member__validateMember(frame,member_entry, password_entry, default_value))

        def __updateMember(self,frame):
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

        def __validateMember(self,frame,member_name,password,role):
            global database
            member_name=member_name.get()
            password=sha3_512(bytes(password.get(),encoding='utf-8',errors='strict')).hexdigest()
            role=role.get()
            #member existance check
            if database._Database__enquiry(member_name):
                showwarning('member',"member already exists use unique name")
                return
            database._Database__insert(frame,member_name,password,role)

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

        def __insert(self,frame,member_name,password,role):
            try:
                if member_name:
                    self.cursor.execute(f"insert into user(user_name,password,role) values('{member_name}','{password}','{role}')")
                    self.database.commit()
                    showinfo("user","details added successfully!")
                    member._Member__createMember(frame)
                else:
                    showwarning('membername',"enter member name first")
            except OperationalError as oe:
                stderr.write(str(oe)+'\n')
                showwarning('database', str(oe))

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

        def __getTables(self):
            user_list=list()
            self.cursor.execute("SELECT * FROM sqlite_master where type='table'")
            for user in self.cursor.fetchall():
                user_list.append(user[1])
            return user_list

        def __getHeader(self,*,table_name):
            self.cursor.execute(f"pragma table_info('{table_name}')")
            return self.cursor.fetchall()

        def __createUserTable(self):
            try:
                self.cursor.execute("create table user(sl integer primary key autoincrement,user_name varchar2(30) unique,password varchar2(80),role varchar2(16))")
                return True
            except OperationalError as oe:
                stderr.write(str(oe)+'\n')
            return False

        def __createDoctorTable(self):
            try:
                self.cursor.execute("create table doctor(sl integer primary key autoincrement,name varchar2(30),specialize_in varchar2(20),timing varchar2(20))")
                return True
            except OperationalError as oe:
                stderr.write(str(oe)+'\n')
            return False

        def __createAppointmentTable(self):
            try:
                self.cursor.execute("create table appointment(sl integer primary key autoincrement,first_time_visit varchar2(3),name varchar2(30),phone varchar2(15),email varchar2(30),appointment_date varchar2(15),doctor_name varchar2(20),specialist_on varchar2(20))")
                return True
            except OperationalError as oe:
                stderr.write(str(oe)+'\n4')
            return False

        def __del__(self):
            self.cursor.close()
            self.database.close()


member=Admin.Member()
maintainance=Admin.Maintainance()
database=Admin.Database()