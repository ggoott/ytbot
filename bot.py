from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from pytube import YouTube

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправь мне ссылку на видео YouTube, и я его скачиваю!')

def download_video(update: Update, context: CallbackContext) -> None:
    url = context.args[0] if context.args else None
    if not url:
        update.message.reply_text('Пожалуйста, предоставь ссылку на видео.')
        return

    try:
        yt = YouTube(url)
        video_stream = yt.streams.get_highest_resolution()
        video_stream.download(output_path='downloads/')
        update.message.reply_text(f'Видео "{yt.title}" скачано!')
    except Exception as e:
        update.message.reply_text(f'Произошла ошибка: {e}')

def main() -> None:
    # Создайте Updater и передайте ему токен вашего бота
    updater = Updater("6892245900:AAE1nZJ4LmY4mB7KiU-5qePNXhSWGXl3t5M")

    # Получите диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Находите и добавьте обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("download", download_video))

    # Запустите бота
    updater.start_polling()

    # Ждите окончания работы
    updater.idle()

if __name__ == '__main__':
    main()
