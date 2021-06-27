
from tkinter import Tk,Label,Button,Entry,PhotoImage
from tkinter.messagebox import showinfo
from sqlite3 import connect,OperationalError
from appointment import Appointment
from doctor import Doctor
from datetime import datetime
from hashlib import sha3_512
from sys import stderr
from admin import Admin

class Login(Tk):
    def __init__(self):
        super().__init__()
        self.title("hospital login")
        self.iconphoto(True,PhotoImage(file='icon/hospital.png'))
        self.geometry("{x}x{y}+{x}+{y}".format(x=self.winfo_screenwidth()//4,y=self.winfo_screenheight()//4))
        self.resizable(False,False)

        #date
        time=Label(self,text=datetime.now(),font=",14,")
        time.grid(row=0,column=1,pady=30)
        #username
        Label(self,text="username",font=',13,').grid(row=1,column=0)
        user_name=Entry(self,highlightcolor='green')
        user_name.grid(row=1,column=1)
        user_name.focus_set()
        #password
        Label(self, text="password", font=',13,').grid(row=2, column=0)
        password=Entry(self,show='*',highlightcolor='green')
        password.grid(row=2, column=1)
        #login button
        img=PhotoImage(file='icon/login.png')
        login=Button(self,text="login",image=img,activebackground='green')
        login.grid(row=3, column=1, sticky='E')
        login.bind('<Button-1>',lambda x:self.authenticate(user_name.get(),password.get()))
        login.bind('<Button-3>',lambda x: self.authenticate(user_name.get(), password.get()))

        self.bind('<Return>',lambda x:self.authenticate(user_name.get(),password.get()))
        self.bind('<KP_Enter>',lambda x:self.authenticate(user_name.get(),password.get()))
        self.update(time)
        self.bind('<Escape>',lambda x:self.destroy())

        self.mainloop()

    def update(self,time):
        time.configure(text=datetime.now())
        time.after(1,lambda:self.update(time))

    def authenticate(self,name,password):
        password=sha3_512(bytes(password,encoding='utf-8',errors='strict')).hexdigest()
        if name.lower()=='admin':
            if password=='8e4a8dcb32209514125ccdfe8c2837a2af7a7c74c39c28355113a02f14b47780d654b73d75db7e9232af2db200bbcc9c06e9accc7b461a65225540812359dc72':
                self.destroy()
                Admin()
            else:
                showinfo("authentication error","admin password mismatch")
            return

        database = connect('database/hospital.db')
        cursor = database.cursor()
        try:
            cursor.execute(f"select * from user where user_name='{name}' and password='{password}'")
            user=cursor.fetchone()[-1]
            if user=='appointment':
                Appointment()
            elif user=='doctor':
                Doctor()
            else:
                showinfo("authentication error","user or password not match please contact to admin")
        except OperationalError as oe:
            stderr.write(str(oe)+'\n')
        finally:
            cursor.close()
            database.close()
if __name__ == '__main__':
    Login()