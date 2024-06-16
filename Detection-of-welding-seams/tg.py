import telebot
import requests
import cv2
import numpy as np
import os
from telebot import types

# Инициализация бота
bot = telebot.TeleBot('6707146959:AAHb0L7gtQ7JfeRnHNcA1_a4hWqGUkmT09Q')

# Приветственное сообщение
privet = "Привет, мой дорогой друг! Я твой чат-бот. Я могу принимать и детектировать дефекты в файлах формата JPG.\nДля начала выберете модель - /select_model"

model = "model1"

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help_(message):
    help_text = "/start - команда запуска бота с приветственным сообщением\n/help - список команд\n/select_model - выбрать модель"
    bot.send_message(message.from_user.id, help_text)

@bot.message_handler(commands=['select_model'])
def select_model(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("YoLOv10😎📊", callback_data="model1")
    button2 = types.InlineKeyboardButton("RTDETR🚀💻", callback_data="model2")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Выберите модель:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["model1", "model2"])
def callback_select_model(call):
    global model
    model = call.data
    bot.send_message(call.message.chat.id, f"Вы выбрали {model}. Отправьте файл формата JPG")
    bot.answer_callback_query(call.id)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, privet)

# Обработчик получения файлов
@bot.message_handler(content_types=['document'])
def handle_file(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        file_extension = message.document.file_name.split('.')[-1].lower()
        
        if file_extension == 'jpg':
            # Скачивание файла
            downloaded_file = bot.download_file(file_info.file_path)
            file_path = f"./{message.document.file_name}"
            
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            
            # Отправка файла на сервер
            addr = 'https://6152-83-143-66-61.ngrok-free.app'
            test_url = addr + '/api/test'
            content_type = 'image/jpeg'
            headers = {'content-type': content_type}
            
            # Чтение и кодирование изображения
            img = cv2.imread(file_path)
            height, width, _ = img.shape  # Получение размеров изображения
            _, img_encoded = cv2.imencode('.jpg', img)
            
            # Отправка запроса
            response = requests.post(test_url, data=img_encoded.tobytes(), headers=headers)
            server_response = response.json() if response.status_code == 200 else {'error': 'Ошибка сервера'}
            
            # Форматирование ответа
            if server_response and not 'error' in server_response:
                names = ["adj", "int", "geo", "pro", "non"]
                
                if model == "model1":
                    colors = {
                        "adj": (255, 0, 0),    # Красный
                        "int": (0, 255, 0),    # Зеленый
                        "geo": (0, 0, 255),    # Синий
                        "pro": (255, 255, 0),  # Желтый
                        "non": (255, 0, 255)   # Фиолетовый
                    }
                elif model == "model2":
                    colors = {
                        "adj": (255, 0, 255),  # Фиолетовый
                        "int": (0, 255, 0),    # Зеленый
                        "geo": (0, 0, 255),    # Синий
                        "pro": (255, 255, 0),  # Желтый
                        "non": (255, 0, 0)     # Красный
                    }
                
                unique_classes = set()
                shift_x, shift_y = -0.02, -0.02  # Сдвиг в относительных координатах (регулируйте эти значения)
                for item in server_response:
                    class_name = names[item['class_id']]
                    unique_classes.add(class_name)
                    
                    # Применение сдвига к относительным координатам
                    rel_x = item['rel_x'] + shift_x
                    rel_y = item['rel_y'] + shift_y
                    rel_x = max(0, min(rel_x, 1))  # Ограничиваем координаты в пределах [0, 1]
                    rel_y = max(0, min(rel_y, 1))
                    
                    # Переводим относительные координаты и размеры в абсолютные
                    start_point = (int(rel_x * width), int(rel_y * height))
                    end_point = (
                        int((rel_x + item['width']) * width),
                        int((rel_y + item['height']) * height)
                    )

                    color = colors[class_name]  # Цвет для класса
                    thickness = 2  # Толщина линии

                    # Отрисовка бокса
                    cv2.rectangle(img, start_point, end_point, color, thickness)

                    # Добавление текста над боксом
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 3
                    font_thickness = 5
                    text_size = cv2.getTextSize(class_name, font, font_scale, font_thickness)[0]
                    text_x = start_point[0]
                    text_y = start_point[1] - 5 if start_point[1] > 15 else start_point[1] + 15  # корректировка текста, чтобы не выходил за пределы изображения
                    
                    cv2.putText(img, class_name, (text_x, text_y), font, font_scale, color, font_thickness)
                
                # Сохраняем изображение с боксами
                output_file_path = f"./processed_{message.document.file_name}"
                cv2.imwrite(output_file_path, img)
                
                # Отправка ответа пользователю
                formatted_response = "Дефекты на изображении: " + ", ".join(unique_classes)
                bot.send_message(message.from_user.id, formatted_response)
                with open(output_file_path, 'rb') as photo:
                    bot.send_photo(message.from_user.id, photo)
                
                # Удаление временного файла
                os.remove(output_file_path)
            else:
                formatted_response = "Нарушений не обнаружено"
                bot.send_message(message.from_user.id, formatted_response)
            
            # Удаление исходного временного файла
            os.remove(file_path)
        else:
            bot.send_message(message.from_user.id, "Пожалуйста, отправьте файл формата JPG.")
    except Exception as e:
        bot.send_message(message.from_user.id, f"Произошла ошибка при обработке файла: {str(e)}")

# Запуск бота
try:
    bot.polling(none_stop=True, interval=0)
except Exception as e:
    print(f"Ошибка при запуске бота: {str(e)}")