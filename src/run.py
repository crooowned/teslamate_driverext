
import os
from dotenv import load_dotenv
from threading import Thread
from telegramframe import TelegramFrame
from data_watcher import Datawatcher
from database import Database

def env(str):
    return os.environ[str]
load_dotenv()

db = Database(env('PG_DB'),env('PG_USER'),env('PG_PASS'),env('PG_HOST'),env('PG_PORT'))
tframe = TelegramFrame(env('TELEGRAM_TOKEN'),  env('TELEGRAM_CHAT_IDS').split(','))
data_watcher = Datawatcher(db, tframe)
tframe.updateDriveHandler = lambda driveId, driverId: data_watcher.updateDrive(driveId, driverId)



def run():
    th = Thread(target=data_watcher.watchDrives)
    th.start()
    tframe.start()
run()
