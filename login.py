
from tkinter import Tk,Label,Button,Entry,PhotoImage
from datetime import datetime
from database.manage import Database

class Login(Tk):
    def __init__(self):
        super().__init__()
        self.database=Database()
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

    def authenticate(self,user_name,user_password):
        print("authentication ",self.database.getLoginDetail(user_name,user_password))

Login()