from re import S
from typing import Callable
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from threading import Thread


class TelegramFrame:
    def __init__(self, botToken, chatIds):
        self.updater = Updater(botToken)
        self.dispatcher = self.updater.dispatcher
        self.chatIds = chatIds
        self.updateDriveHandler = None

    def start(self):
        self.dispatcher.add_handler(CallbackQueryHandler(self.__callbackHandler))
        self.updater.start_polling()
        print('Idling...')
        self.updater.idle()

    def askForDrive(self, drive, drivers):
        for chatId in self.chatIds:
            self.updater.bot.send_message(chat_id=chatId, text=self.__getText(drive),  reply_markup=self.__getKeyboard(drive.id, drivers))
    
    def __callbackHandler(self, update: Update, context: CallbackContext):
        print('Callback received')
        query = update.callback_query
        driveId = int(query.data.split(':')[0])
        driverId = int(query.data.split(':')[1])
        self.updateDriveHandler(driveId, driverId)
        query.answer("Fahrer gespeichert!")

    def __getText(self, drive):
        return "Neue Fahrt 🚙 erkannt!\n🚀Distanz: " + str(round(drive.distance,2)) + "km\n⏳Dauer: " + str(round(drive.minutes/60,2)) + "h (" + str(round(drive.minutes,2)) + "min)\n📍Start: " + str(drive.start_location['display_name']) + "\n🏁Ende: " + str(drive.end_location['display_name'] + "\nBitte wählen Sie einen Fahrer aus:")

    def __getKeyboard(self, driveId, drivers):
        keyboard = []
        for driver in drivers:
            keyboard.append([InlineKeyboardButton(str(driver[1]), callback_data=str(driveId)+":"+str(driver[0]))])
        return InlineKeyboardMarkup(keyboard)