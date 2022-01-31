from time import sleep
from json import dumps,loads

from telegramframe import TelegramFrame

class Datawatcher:
    def __init__(self, db, telegram: TelegramFrame):
        self.cachedDrives = self.__loadCache()
        self.telegram = telegram
        self.db = db

    def watchDrives(self):
        self.__migrateDatabase()
        while(True):
            drives = self.db.queryFetchAll("SELECT d.*, sa.raw, sa2.raw FROM drives d LEFT JOIN addresses sa ON sa.id = d.start_address_id LEFT JOIN addresses sa2 ON sa2.id = d.end_address_id WHERE d.driverid IS NULL order by d.start_date asc;")
            print('New Drives: ' + str(len(drives)))
            for drive in drives:
                if(drive[0] not in self.cachedDrives):
                    print('New drive: ' + str(drive[0]))
                    if(drive[2] is None):
                        self.cachedDrives.append(drive[0])
                        self.__saveCache()
                        continue
                    d = Drive(drive[0], drive[1], drive[2], drive[11], drive[12], drive[24], drive[25])
                    self.telegram.askForDrive(d, self.__getDrivers())
                    sleep(5)
                    self.cachedDrives.append(drive[0])
                    self.__saveCache()
            sleep(60*5) # 5min

    def updateDrive(self, driveId, driverId):
        self.db.query("UPDATE drives SET driverid = " + str(driverId) + " WHERE id = " + str(driveId) + ";")

    def __migrateDatabase(self):
        self.db.query("CREATE TABLE IF NOT EXISTS drivers (driverid SERIAL PRIMARY KEY, name character varying not null);")
        self.db.query("ALTER TABLE drives ADD COLUMN IF NOT EXISTS driverid integer;")

    def __saveCache(self):
        arr = dumps(self.cachedDrives)
        with open('src/data/cache.json', 'w+') as f:
            f.write(arr)
        f.close()

    def __getDrivers(self):
        return self.db.queryFetchAll("SELECT * FROM drivers;")

    def __loadCache(self):
        try:
            with open('src/data/cache.json', 'r') as f:
                return loads(f.read())
        except:
            return []
class Drive:
    def __init__(self, id, startdate, enddate, distance, minutes, start_location, end_location) -> None:
        self.id = id
        self.startdate = startdate
        self.enddate = enddate
        self.distance = distance or 0
        self.minutes = minutes or 0
        self.start_location = start_location
        self.end_location = end_location

    def getStartLocationDisplayname(self):
        return self.start_location.get('display_name')

    def getEndLocationDisplayname(self):
        return self.end_location.get('display_name')