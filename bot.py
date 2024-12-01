import logging
import os
import asyncio
import aiohttp
import json
import nest_asyncio  
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes,CallbackContext
from dotenv import load_dotenv
from datetime import datetime
import pytz
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, PicklePersistence

from menu import main_menu, handle_menu_navigation  # Добавляем импорт из файла меню
from state import bot_state


# Настраиваем постоянное хранилище
persistence = PicklePersistence(filepath="bot_data.pkl")


#from keyboard.menu import main_menu, handle_menu_navigation  # Добавляем импорт из файла меню
# Словари для перевода дней недели и месяцев
days_of_week = {
    "Monday": "понедельник",
    "Tuesday": "вторник",
    "Wednesday": "среда",
    "Thursday": "четверг",
    "Friday": "пятница",
    "Saturday": "суббота",
    "Sunday": "воскресенье"
}

months = {
    "January": "января",
    "February": "февраля",
    "March": "марта",
    "April": "апреля",
    "May": "мая",
    "June": "июня",
    "July": "июля",
    "August": "августа",
    "September": "сентября",
    "October": "октября",
    "November": "ноября",
    "December": "декабря"
}




# Создаем множество для хранения ID каналов-доноров
donor_channels: set[str] = set()

nest_asyncio.apply()

# In-memory storage for donor channels
donor_channels = set()

# Load environment variables
load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
owner_id = int(os.getenv('OWNER_ID'))
forward_to_channel = os.getenv('FORWARD_TO_CHANNEL')

# Загружаем список каналов из переменной окружения FORWARD_FROM_CHANNEL
forward_from_channel_raw = os.getenv('FORWARD_FROM_CHANNEL', '')
donor_channels = set(forward_from_channel_raw.split(',')) if forward_from_channel_raw else set()
ollama_url = os.getenv('OLLAMA_URL')

def get_random_emotion():
    # Получаем строку эмоций из .env и создаем список
    emotions = os.getenv("EMOTIONS", "")
    emotions_list = [emotion.strip() for emotion in emotions.split(",") if emotion.strip()]
    return random.choice(emotions_list) if emotions_list else "радость"  # Используем "радость" как значение по умолчанию

# Инициализируем выбранную эмоцию при запуске
emotion = get_random_emotion()

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Главное меню:", reply_markup=main_menu())

# Функция для тестирования подключения к Ollama
async def test_ollama_connection():
    models = await get_ollama_models()
    if models:
        logging.info("Подключение к Ollama успешно. Список моделей получен.")
        return True
    else:
        logging.error("Ошибка подключения к Ollama: не удалось получить список моделей.")
        return False



async def get_ollama_response(message, context):
    temperature = bot_state.temperature
    logging.info(f"Используем глобальную температуру из bot_state: {temperature}")
    logging.info(f"Используем глобальную температуру: {temperature}")
        
    logging.info(f"Using temperature: {temperature}")

   

#async def get_ollama_response(message, context=None):

#    if not context or not context.user_data:
#        temperature = 0.8  # Значение по умолчанию
#    else:
#        temperature = context.user_data.get("temperature", 0.8)
    
    logging.info(f"Температура, переданная в запрос: {temperature}")  # Логируем значение температуры
    url = f'{ollama_url}/api/generate'
    headers = {
    'Content-Type': 'application/json',
    }
    # Инициализируем emotion для всех случаев
    emotion = get_random_emotion()

        
        # Проверяем, начинается ли сообщение с "!"
    if message.startswith("!"):
        # Используем сообщение без дополнительной информации
        prompt = message[1:].strip()  # Убираем "!" и возможные пробелы
        
    else:
        moscow_tz = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(moscow_tz)
        day_of_week_en = current_time.strftime("%A")
        month_name_en = current_time.strftime("%B")
        day_of_week = days_of_week.get(day_of_week_en, day_of_week_en)
        month_name = months.get(month_name_en, month_name_en)

        day_of_month = current_time.strftime("%d").lstrip("0")
        year = current_time.strftime("%Y")
        time_str = current_time.strftime("%H:%M:%S")


        prompt = (f"Сегодня {day_of_week}, {day_of_month} {month_name} {year} года, {time_str}. "
                  f"Прокомментируй событие с юмором и эмоцией {emotion} с использованием emoji: {message}")

    

    logging.info(f"Sending prompt to Ollama: {prompt}, {temperature}")

    # data = {
        # 'model': 'Jann_Max',
        # 'keep_alive': 30,
        # 'prompt': prompt,
        # "options": {
            # "temperature": temperature
 # #           "num_thread": 16
        # },
        # "stream": False
    # }

    
    data = {
        'model': 'Jann_Max',
        'prompt': prompt,
        "stream": False
    }
    
    # data = {
        # 'model': 'Jann_Max',
        # 'prompt': prompt,
        # "options": {
            # "temperature": temperature,
            # "num_thread": 16
            
        # },
        # "stream": False
    # }
    logging.error(f"полный запрос {data} ")     
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    full_response = ""
                    async for line in response.content:
                        try:
                            response_part = json.loads(line)
                            full_response += response_part.get('response', '')
                        except json.JSONDecodeError as e:
                            logging.error(f"Ошибка декодирования JSON: {e}, строка: {line.decode()}")
                            return f"Ошибка декодирования ответа от Ollama: {e}"


                    return full_response, emotion  
                   
                else:
                    error_text = await response.text()
                    logging.error(f"Ошибка запроса: {response.status}, {error_text}")
                    return f"Ошибка: {response.status}. Ответ от Ollama: {error_text}"
    except aiohttp.ClientError as e:
        logging.error(f"Ошибка при подключении: {e}")
        return f"Ошибка при подключении к Ollama: {e}"
    
    
async def send_startup_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    # Проверяем подключение к Ollama и получаем ответ
    connection_successful = await test_ollama_connection()


    if connection_successful:
        # Если подключение успешно, отправляем сообщение о запуске
       # ollama_response = await get_ollama_response("!Пошути про обитателей дома")  # Запрашиваем шутку для примера
        startup_message = f'📢Бот готов к работе.' #\n\n Шутка от Ollama: {ollama_response}'
    else:
        # Если подключение не удалось, сообщаем об этом
        startup_message = '📢Бот готов к работе, но не удалось подключиться к Ollama.'

    await context.bot.send_message(chat_id=forward_to_channel, text=startup_message)



async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"handle_all_messages called for update: {update}")
    
    if update.channel_post:
        logger.info(f"Channel post detected: {update.channel_post}")
        channel = update.channel_post.chat
        channel_identifier = str(channel.id)

        logger.info(f"Current channel identifier: {channel_identifier}")
        logger.info(f"Current donor channels: {donor_channels}")

        # Проверяем, является ли сообщение ответом от Ollama
        if "📢" in update.channel_post.text:
            logger.info("Ignoring message from Ollama.")
            return  # Игнорируем это сообщение

        if channel_identifier in donor_channels:
            try:
                original_text = update.channel_post.text
                logger.info(f"Sending to Ollama: {original_text}")
	            
	            # Явно передаем context в get_ollama_response
                ollama_response, emotion = await get_ollama_response(original_text, context=context)
                logger.info(f"Received from Ollama: {ollama_response}")


                message_text = (
                    f"📢🤖 Комментарий вУмного дома <tg-spoiler><b>(с эмоцией {emotion})</b></tg-spoiler>:\n {ollama_response}"
                )


              # Отправка сообщения с указанным режимом разметки
                await context.bot.send_message(
                    chat_id=forward_to_channel,
                    text=message_text,
                    parse_mode='HTML'
)

                logger.info(f"Successfully forwarded message to {forward_to_channel}")
           
            except Exception as e:
                error_message = (
                    f"❌ Ошибка при обработке сообщения:\n"
                    f"Канал: {channel.title}\n"
                    f"Ошибка: {str(e)}"
                )
                await context.bot.send_message(
                    chat_id=forward_to_channel,
                    text=error_message
                )
                logger.error(f"Error processing message: {e}", exc_info=True)



async def log_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Received update type: {update.update_id}")
    if update.message:
        logger.info(f"Message from {update.message.from_user.id}: {update.message.text}")
        if hasattr(update.message, 'forward_origin'):
            logger.info(f"Message is forwarded from: {update.message.forward_origin}")
        else:
            logger.info("Message is not forwarded")
    elif update.channel_post:
        logger.info(f"Channel post in {update.channel_post.chat.id}: {update.channel_post.text}")

    else:
        logger.info(f"Received update: {update}")

def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Exception while handling an update: {context.error}")



async def get_ollama_models():
    url = f'{ollama_url}/api/tags'
    headers = {'Content-Type': 'application/json'}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    models = [model["name"] for model in result.get("models", [])]
                    return models
                else:
                    error_text = await response.text()
                    logger.error(f"Ошибка при получении списка моделей от Ollama: {response.status}, {error_text}")
                    return []
    except aiohttp.ClientError as e:
        logger.exception(f"Ошибка подключения к Ollama для получения списка моделей: {str(e)}")
        return []


async def debug_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отладочная функция для логирования всех входящих сообщений"""
    logger.debug("=== New Message Debug ===")
    logger.debug(f"Update object: {update.to_dict()}")
    if update.message:
        logger.debug(f"Message text: {update.message.text}")
        

        if update.message.forward_origin:
            logger.debug(f"Forward info: {update.message.forward_origin}")
    elif update.channel_post:
        logger.debug(f"Channel post: {update.channel_post.text}")
        logger.debug(f"Channel info: {update.channel_post.chat}")
    logger.debug("========================")



async def main() -> None:
    try:
        # Проверяем подключение к Ollama при запуске
        if not await test_ollama_connection():
            logger.error("Не подключились к Ollama.")
            return

        # Создаем приложение
        application = ApplicationBuilder().token(bot_token).persistence(persistence).build()
                
        application.add_handler(CommandHandler("start", start))  # Обработчик для команды старт
        application.add_handler(CallbackQueryHandler(handle_menu_navigation))  # Обработчик для меню навигации
        # Добавляем обработчики

        application.add_handler(MessageHandler(filters.ALL, debug_message), group=-2)
        application.add_handler(MessageHandler(filters.ALL, log_update), group=-1)
        application.job_queue.run_once(send_startup_message, 1)

        application.add_handler(MessageHandler(filters.ALL, handle_all_messages))
        
        application.add_error_handler(error_handler)

        
        
        logger.info("All handlers added successfully")
        logger.info("Starting polling...")

        # Запускаем бота
        await application.run_polling(drop_pending_updates=True)

    except Exception as e:
        logger.error(f"Error during bot execution: {e}", exc_info=True)
        raise

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot stopped due to error: {e}", exc_info=True)
        
 