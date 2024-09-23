import telebot
import yt_dlp
from telebot import types

API_TOKEN = '6892245900:AAE1nZJ4LmY4mB7KiU-5qePNXhSWGXl3t5M'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Send a YouTube link to download the video!")

@bot.message_handler(func=lambda message: message.text.startswith('https://youtu.be/'))
def download_video(message):
    link = message.text
    ydl_opts = {'outtmpl': '%(title)s.%(ext)s'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(link, download=False)
            file_name = ydl.prepare_filename(info)
            ydl.download([link])
            with open(file_name, 'rb') as file:
                bot.send_video(message.chat.id, file, caption="Video downloaded!")
        except yt_dlp.utils.DownloadError as e:
            bot.reply_to(message, f"Error: {e}. Try checking the YouTube link or updating yt_dl.")

bot.polling()
