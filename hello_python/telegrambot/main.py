import os 
import telebot
from dotenv import load_dotenv
from funcion import obtener_bcv

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome (message):
  bot.reply_to(message, "Epale mi loco todo bello ? ")

@bot.message_handler(commands=['Dolar_BCV', 'BCV'])
def send_welcome (message):
  bot.reply_to(message, f'El valor del dolar de hoy es: {obtener_bcv()}' )

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()