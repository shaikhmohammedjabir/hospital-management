
from tkinter import Tk,Label,Button,Entry,PhotoImage
from datetime import datetime

class Login(Tk):
    def __init__(self):
        super().__init__()
        self.title("hospital login")
        self.iconphoto(True,PhotoImage(file='icon/hospital.png'))
        self.geometry("{x}x{y}+{x}+{y}".format(x=self.winfo_screenwidth()//4,y=self.winfo_screenheight()//4))
        self.resizable(False,False)

        time=Label(self,text=datetime.now(),font=",14,")
        time.grid(row=0,column=1,pady=30)
        Label(self,text="username",font=',13,').grid(row=1,column=0)
        Entry(self).grid(row=1,column=1)
        Label(self, text="password", font=',13,').grid(row=2, column=0)
        Entry(self,show='-').grid(row=2, column=1)
        img=PhotoImage(file='icon/login.png')
        login=Button(self,text="login",image=img)
        login.grid(row=3, column=1, sticky='E')


        self.update(time)
        self.bind('<Escape>',lambda x:self.destroy())
        self.mainloop()
    def update(self,time):
        time.configure(text=datetime.now())
        time.after(1,lambda:self.update(time))


Login()