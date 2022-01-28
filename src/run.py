from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import psycopg2
import os
from dotenv import load_dotenv

TELEGRAMTOKEN=os.environ['TELEGRAM_TOKEN']
db = None
load_dotenv()

def env(str):
    return os.environ[str]

conn = psycopg2.connect("dbname="+env('PG_DB')+" user=" + env('PG_USER') + " password=" + env('PG_PASS') + " host=" + env('PG_HOST') + ' port=' + env('PG_PORT'))

def run():
    print('Connecting to bot')
    updater = Updater(TELEGRAMTOKEN)
    dispatcher = updater.dispatcher
    updater.start_polling()
    updater.idle()

run()
