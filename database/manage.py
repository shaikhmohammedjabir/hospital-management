
from sqlite3 import connect,OperationalError
from sys import stderr

class Database:
    def __init__(self):
        self._database=connect('hospital.db')
        self._cursor=self._database.cursor()

    def getLoginDetail(self,user_name,user_password):
        try:
            self._cursor.execute(f"select * from user where name={user_name} and password={user_password}")
            return self._cursor.fetchone()[-1]
        except OperationalError as oe:
            stderr.write(str(oe)+'\n')