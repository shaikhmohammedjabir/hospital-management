
from tkinter import Tk,Label,Button,Entry,PhotoImage
from tkinter.messagebox import showinfo
from sqlite3 import connect,OperationalError
from datetime import datetime
from sys import stderr

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
        user_name=Entry(self)
        user_name.grid(row=1,column=1)
        #password
        Label(self, text="password", font=',13,').grid(row=2, column=0)
        password=Entry(self,show='*')
        password.grid(row=2, column=1)
        #login button
        img=PhotoImage(file='icon/login.png')
        login=Button(self,text="login",image=img,activebackground='green')
        login.grid(row=3, column=1, sticky='E')
        login.bind('<Button-1>',lambda x:self.authenticate(user_name,password))
        login.bind('<Button-3>',lambda x: self.authenticate(user_name, password))

        self.bind('<Return>',lambda x:self.authenticate(user_name,password))
        self.bind('<KP_Enter>',lambda x:self.authenticate(user_name,password))
        self.update(time)
        self.bind('<Escape>',lambda x:self.destroy())
        self.mainloop()

    def update(self,time):
        time.configure(text=datetime.now())
        time.after(1,lambda:self.update(time))

    def authenticate(self,user_name,user_password):
        database = connect('database/hospital.db')
        cursor = database.cursor()
        try:
            cursor.execute(f"select * from user where name='{user_name.get()}' and password='{user_password.get()}'")
            user=cursor.fetchone()
            if user:
            #    return user[-1]
                print(user)
            else:
                showinfo("authentication error","user not exists please contact to admin")
        except OperationalError as oe:
            stderr.write(str(oe)+'\n')
        finally:
            cursor.close()
            database.close()

Login()