import asyncio
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import nest_asyncio

# Применяем nest_asyncio для совместимости с Jupyter Notebook и другими асинхронными средами
nest_asyncio.apply()

# Установите уровень логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Вставьте ваш токен
TOKEN = '7294619798:AAFdrXkw5QPm9tXVvRUnvfTxToZq3aFkIzI'

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Отправь мне фото, и я верну его тебе обратно.')

# Обработчик для фотографий
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Получаем объект файла фото
    photo = update.message.photo[-1]
    
    # Получаем файл фото и отправляем его обратно
    file = await context.bot.get_file(photo.file_id)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=file.file_id)

    # Логирование для проверки
    logging.info(f"Фото отправлено обратно с file_id: {file.file_id}")

# Основная функция для запуска бота
async def main():
    # Создаем приложение
    application = ApplicationBuilder().token(TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Запускаем приложение
    await application.start()
    await application.updater.start_polling()
    
    # Ждем пока приложение работает
    await application.wait_until_stopped()

if __name__ == '__main__':
    asyncio.run(main())

