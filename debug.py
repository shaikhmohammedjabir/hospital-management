

#create table user(sl integer primary key autoincrement,user_name varchar2(30) unique,password varchar2(80),role varchar2(16))


from database.manage import *



class Test:
    def __init__(self):
        print("class started")

    def _chew(self):
        print("function chewing")

    def __del__(self):
        print("function going to die")

t=Test()
t._chew()