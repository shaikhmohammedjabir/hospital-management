
#:todo write testing code here
"create table user(sl integer primary key autoincrement,user_name varchar2(30) unique,password varchar2(80),role varchar2(16))"

import sqlite3


database=sqlite3.connect('database/hospital.db')
cursor=database.cursor()
cursor.execute("SELECT * FROM sqlite_master where type='table'")
for user in cursor.fetchall():
    print(user[1])

cursor.close()
database.close()
