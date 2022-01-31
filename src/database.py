from sqlite3 import OperationalError
from time import sleep
import psycopg2

class Database:
    def __init__(self, db, user, password, host, port):
        self.db = db
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.__connect()

    def __connect(self):
        try:
            self.database = psycopg2.connect("dbname=" + self.db + " user=" + self.user + " password=" + self.password  + " host=" + self.host + ' port=' + self.port)
        except:
            print('error connecting to db retrying...')
            sleep(5)
            self.__connect()
    
    def queryFetchAll(self, sql, params = ()):
        cur = self.__execute(sql, params)
        return cur.fetchall()

    def query(self, sql, params = ()):
        self.__execute(sql, params)
        self.database.commit()

    def __execute(self, sql, params = ()):
        try:
            cur = self.database.cursor()
            cur.execute(sql, params)
            return cur
        except:
            self.__connect()
            print('renewing connection to db')
            sleep(5)
            return self.__execute(sql, params)