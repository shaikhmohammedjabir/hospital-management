
from sqlite3 import connect,OperationalError
from sys import stderr

class Database:
    database=connect('hospital.db')
    cursor=database.cursor()
    def getLoginDetail(self,user_name,user_password):
        try:
            sql=f"select * from user where name='{user_name}' and password='{user_password}'"
            print(sql)
            Database.cursor.execute(sql)
            user=Database.cursor.fetchone()
            if user:
                return user
            return None
        except OperationalError as oe:
            stderr.write(str(oe)+'\n')

    def closeDatabase(self):
        Database.cursor.close()
        Database.database.close()
        return True