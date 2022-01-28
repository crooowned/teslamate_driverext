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
        self.database = psycopg2.connect("dbname=" + self.db + " user=" + self.user + " password=" + self.password  + " host=" + self.host + ' port=' + self.port)

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
        except psycopg2.OperationalError as e:
            self.__connect()
            print('renewing connection to db')
            return self.__execute(sql, params)