import telebot
import yt_dlp
import os

API_TOKEN = '6892245900:AAE1nZJ4LmY4mB7KiU-5qePNXhSWGXl3t5M'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне ссылку на видео YouTube, и я помогу тебе его скачать.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    bot.reply_to(message, "Начинаю загрузку...")

    # Параметры загрузки
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'webm',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info['title']
            filename = f"{title}.webm"
            print(f"Скачиваемое имя файла: {filename}")

            # Сжимаем видео перед отправкой
            compressed_filename = f"compressed_{filename}"
            ffmpeg_command = f"ffmpeg -i \"{filename}\" -vcodec libx264 -crf 28 -preset ultrafast \"{compressed_filename}\""
            print(f"Выполняем команду: {ffmpeg_command}")

            if os.system(ffmpeg_command) != 0:
                raise Exception("Ошибка при сжатии видео")

            print(f"Отправляем видео: {compressed_filename}")
            # Отправка видео пользователю
            with open(compressed_filename, 'rb') as video:
                bot.send_video(message.chat.id, video, caption=f"Загрузка завершена: {title}")

            # Удаление видео после отправки
            os.remove(filename)
            os.remove(compressed_filename)
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")
        print(f"Ошибка: {str(e)}")

if __name__ == '__main__':
    bot.polling()
