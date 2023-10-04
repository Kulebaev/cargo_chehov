import os
from django import setup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cargo_chehov.settings")
setup()

import telebot
from django.core.files import File
from landing.models import Car, CarImage
from io import BytesIO

TOKEN = '6451444836:AAHJu-3gGdsMreMm_QPkkDsOiJjb4T_xIyE'

bot = telebot.TeleBot(TOKEN)

# Словарь для отслеживания соответствия между ID чата и ID машины
chat_car_ids = {}
# Словарь для отслеживания типа файла, который ожидается
chat_file_types = {}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id

    # Просим пользователя отправить наименование машины
    bot.send_message(chat_id, "Пожалуйста, напишите название машины.")

@bot.message_handler(func=lambda message: True 
                     and not message.text.lower() == '/start'
                     and not '/exit' in message.text.lower())
def receive_title(message):
    chat_id = message.chat.id

    if chat_id in chat_car_ids:
        if chat_file_types[chat_id] == "description":
            receive_description(message)
            return
        elif chat_file_types[chat_id] == "image":
            bot.send_message(chat_id, "Вы уже начали процесс добавления машины. Пожалуйста, отправьте файлы картинок.")
        

    # Извлекаем название машины из сообщения
    title = message.text

    # Создаем запись в базе данных
    car_entry = Car(title=title)
    car_entry.save()

    # Сохраняем соответствие между ID чата и ID машины
    chat_car_ids[chat_id] = car_entry.id

    # Просим пользователя отправить описание машины
    bot.send_message(chat_id, "Теперь отправьте описание машины.")

    # Устанавливаем ожидание описания машины
    chat_file_types[chat_id] = "description"


def receive_description(message):
    chat_id = message.chat.id

    if chat_id in chat_car_ids:
        description = message.text

        # Получаем ID машины из chat_car_ids
        car_id = chat_car_ids.get(chat_id)

        if car_id is not None:
            # Сохраняем описание машины
            car_entry = Car.objects.get(id=car_id)
            car_entry.descriptions = description
            car_entry.save()

            # Просим пользователя отправить картинки машины
            bot.send_message(chat_id, "Теперь отправьте картинки машины.")

            # Устанавливаем ожидание файлов с изображениями
            chat_file_types[chat_id] = "image"

@bot.message_handler(content_types=['photo'])
def receive_files(message):
    chat_id = message.chat.id

    if chat_id not in chat_file_types:
        bot.send_message(chat_id, 'Неожиданное сообщение. Пожалуйста, начните снова с команды /start.')
        return

    if message.photo:
        file_info = bot.get_file(message.photo[-1].file_id)
        file = bot.download_file(file_info.file_path)

        # Получаем ID машины из chat_car_ids
        car_id = chat_car_ids.get(chat_id)

        if car_id is not None:
            # Сохраняем файлы изображений в модель CarImage
            with BytesIO(file) as file_buffer:
                car_image = CarImage()
                car_image.file.save(file_info.file_id, File(file_buffer))
                car_image.save()

                # Добавляем изображение к списку изображений машины
                car_entry = Car.objects.get(id=car_id)
                car_entry.image.add(car_image)
            bot.send_message(chat_id, 'Картинки успешно добавленны! Если хотите добавить ещё машины напишите /start')
            return

    bot.send_message(chat_id, 'Не найдена связь с машиной. Пожалуйста, начните снова с команды /start.')

@bot.message_handler(commands=['exit'])
def exit(message):
    chat_id = message.chat.id
    print(chat_id)
    if chat_id in chat_car_ids:
        # Удаляем соответствие между ID чата и ID машины
        del chat_car_ids[chat_id]

    if chat_id in chat_file_types:
        # Удаляем соответствие между ID чата и типом файла
        del chat_file_types[chat_id]

    bot.send_message(chat_id, "Вы можете добавить новую машину. Напишите название машины.")

bot.polling(none_stop=True)
