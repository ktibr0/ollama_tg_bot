# menu.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import logging
import platform
import psutil
from datetime import timedelta
from state import bot_state




# Главное меню
def main_menu():
    keyboard = [
        [InlineKeyboardButton("Управление моделями", callback_data='manage_models')],
        [InlineKeyboardButton("Управление генерацией", callback_data='manage_generation')],
        [InlineKeyboardButton("Информация о системе", callback_data='system_info')],  # Новая кнопка
        [InlineKeyboardButton("Другие настройки", callback_data='other_settings')]
    ]
    return InlineKeyboardMarkup(keyboard)


# Подменю управления моделями
def manage_models_menu():
    keyboard = [
        [InlineKeyboardButton("Список моделей", callback_data='list_models')],
        [InlineKeyboardButton("Выбрать модель", callback_data='choose_model')],
        [InlineKeyboardButton("Удалить модель", callback_data='delete_model')],
        [InlineKeyboardButton("Создать модель", callback_data='create_model')],
        [InlineKeyboardButton("Назад", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Подменю создания модели
def create_model_menu():
    keyboard = [
        [InlineKeyboardButton("Указать системный промпт", callback_data='set_prompt')],
        [InlineKeyboardButton("Исходная модель", callback_data='base_model')],
        [InlineKeyboardButton("Назад", callback_data='back_to_manage_models')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Подменю управления генерацией
def manage_generation_menu():
    keyboard = [
        [InlineKeyboardButton("Промпт", callback_data='generation_prompt')],
        [InlineKeyboardButton("Характер", callback_data='generation_character')],
        [InlineKeyboardButton("Температура", callback_data='generation_temperature')],  # Кнопка выбора температуры
        [InlineKeyboardButton("Потоки", callback_data='generation_threads')],
        [InlineKeyboardButton("Назад", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)


# Подменю других настроек
def other_settings_menu():
    keyboard = [
        [InlineKeyboardButton("Интервал между шутками", callback_data='joke_interval')],
        [InlineKeyboardButton("Назад", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Обработчик для навигации по меню


async def handle_menu_navigation(update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'system_info':
        # Получение системной информации
        system_info = {
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "cpu_usage": psutil.cpu_percent(),
            "cpu_count": psutil.cpu_count(logical=True),
            "disk_usage": psutil.disk_usage('/').percent,
            "memory_usage": psutil.virtual_memory().percent,
            "uptime": str(timedelta(seconds=int(psutil.boot_time())))
        }

        # Формирование сообщения
        status_message = (
            f"🖥 Система: {system_info['platform']}\n"
            f"🐍 Python: {system_info['python_version']}\n"
            f"⚡️ CPU: {system_info['cpu_usage']}%\n"
            f"💾 RAM: {system_info['memory_usage']}%\n"
            f"💾 Количество потоков: {system_info['cpu_count']}\n"
            f"💾 Использование диска: {system_info['disk_usage']}%\n"
            f"⏱ Время работы: {system_info['uptime']}\n\n"
        )




        await query.edit_message_text(status_message)
        return


    if query.data == 'generation_temperature':
        current_temperature = bot_state.temperature
        await query.edit_message_text(
            f"Выберите температуру. Сейчас установлена {current_temperature}",
            reply_markup=choose_temperature_menu()
        )
        return

    elif query.data.startswith('set_temp_'):
        selected_temperature = float(query.data.split('_')[2])
        bot_state.temperature = selected_temperature
        logging.info(f"Установлена новая температура в bot_state: {selected_temperature}")
        await query.edit_message_text(
            f"Температура установлена на {selected_temperature}",
            reply_markup=manage_generation_menu()
        )
        return   
    if query.data == 'manage_models':
        await query.edit_message_text("Управление моделями:", reply_markup=manage_models_menu())
    elif query.data == 'manage_generation':
        await query.edit_message_text("Управление генерацией:", reply_markup=manage_generation_menu())
    elif query.data == 'other_settings':
        await query.edit_message_text("Другие настройки:", reply_markup=other_settings_menu())
    elif query.data == 'list_models':
        await context.bot.send_message(query.message.chat_id, "Список моделей...")  # Заглушка для примера
    elif query.data == 'choose_model':
        await context.bot.send_message(query.message.chat_id, "Выбор модели...")  # Заглушка для примера
    elif query.data == 'delete_model':
        await context.bot.send_message(query.message.chat_id, "Удаление модели...")  # Заглушка для примера
    elif query.data == 'create_model':
        await query.edit_message_text("Создание модели:", reply_markup=create_model_menu())
    elif query.data == 'back_to_main':
        await query.edit_message_text("Главное меню:", reply_markup=main_menu())
    elif query.data == 'back_to_manage_models':
        await query.edit_message_text("Управление моделями:", reply_markup=manage_models_menu())
    else:
        await query.edit_message_text("Опция в разработке.")



def choose_temperature_menu():
    keyboard = [
        [InlineKeyboardButton("0.2", callback_data='set_temp_0.2')],
        [InlineKeyboardButton("0.4", callback_data='set_temp_0.4')],
        [InlineKeyboardButton("0.6", callback_data='set_temp_0.6')],
        [InlineKeyboardButton("0.8", callback_data='set_temp_0.8')],
        [InlineKeyboardButton("1.0", callback_data='set_temp_1.0')],
        [InlineKeyboardButton("Назад", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)
    
    
    
