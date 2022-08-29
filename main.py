import os

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater

import weather
from utility import SMILE

load_dotenv()

updater = Updater(os.getenv('TOKEN'))
chat_id = os.getenv('CHAT_ID')

def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/Amguema'],['/Egvekinot']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text=('Привет, {}. Нажми на кнопку поселка, погоду в котором ты хочешь'
             f' узнать').format(name),
        reply_markup=button
    )


updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(CommandHandler('Amguema', weather.new_weather))
updater.dispatcher.add_handler(CommandHandler('Egvekinot', weather.new_weather))

updater.start_polling()
updater.idle()