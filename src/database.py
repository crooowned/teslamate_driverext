import psycopg2

class Database:
    def __init__(self, db, user, password, host, port):
        self.database = psycopg2.connect("dbname=" + db + " user=" + user + " password=" + password  + " host=" + host + ' port=' + port)

    def queryFetchAll(self, sql, params = ()):
        cur = self.database.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

    def query(self, sql, params = ()):
        cur = self.database.cursor()
        cur.execute(sql, params)
        self.database.commit()