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

@bot.message_handler(commands=['ahomi'])
def send_message(message):
    # 1. Guarda la ruta de la imagen en una variable
    ruta_imagen = r"hello_python\telegrambot\assets\cat_with_rose.jpeg"
    
    # 2. Guarda el texto que quieres enviar en otra variable
    texto_del_mensaje = "Hola esto es una prueba del bot, pero quiero agradecerte por tomarte las molestias de haber interactuado con el. Te quiero mucho y me encantas preciosa ♥️✨"

    try:
        # 3. Abre el archivo de la imagen en modo lectura binaria ('rb')
        with open(ruta_imagen, 'rb') as foto:
            # 4. Usa bot.send_photo() para enviar la imagen con el texto como caption
            bot.send_photo(message.chat.id, foto, caption=texto_del_mensaje)

    except FileNotFoundError:
        # En caso de que la ruta del archivo sea incorrecta, envía un mensaje de error
        bot.reply_to(message, "Lo siento, no pude encontrar la imagen para enviarla.")
    except Exception as e:
        # Para cualquier otro error
        print(f"Ocurrió un error: {e}")
        bot.reply_to(message, "Hubo un problema al intentar enviar la imagen.")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)





bot.infinity_polling()