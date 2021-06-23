
from sqlite3 import connect,OperationalError
from sys import stderr

class Database:
    def __init__(self):
        self.database=connect('hospital.db')
        self.cursor=self.database.cursor()

    def getLoginDetail(self,user_name,user_password):
        try:
            self.cursor.execute(f"select * from user where name='{user_name}' and password='{user_password}'")
            user=self.cursor.fetchone()
            print(user)
            if user:
                return user[-1]
            return None
        except OperationalError as oe:
            stderr.write(str(oe)+'\n')

    def closeDatabase(self):
        self.cursor.close()
        self.database.close()
        return True

