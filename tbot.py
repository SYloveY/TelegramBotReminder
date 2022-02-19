# Импортируем библиотеку pyTelegramBotAPI
import telebot
from telebot import types
# Импортируем наш конфиг, где указан Токен нашего бота
import config
# Импортируем модуль Time, для задержки отправки нашего сообщения
import time

# Переменная для сохранения текста напоминания
rm_text = ''
# Переменная для сохранения времени напоминания
rm_time = 0

# Переменная нашего бота
bot = telebot.TeleBot(config.TOKEN)


# Создание обработчика команды /start
@bot.message_handler(commands=['start'])
def welcome(message):
    # Создаем переменную, которая открывает наш файл с изображением
    st = open('img/welcome_img.webp', 'rb')
    # Бот отправляет в чат наше изображение
    bot.send_sticker(message.chat.id, st)
    # Создаем переменную, которая открывает наш файл с музыкой
    mu = open('music/welcom_music.ogg', 'rb')
    # Бот отправляет в чат наш звук
    bot.send_audio(message.chat.id, mu)


# Создание обработчика сообщений
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    # Создаем условие, если человек здоровается с ботом
    if message.text == 'Привет' or message.text == 'привет':
        # Бот здоровается в ответ
        bot.reply_to(message, 'Привет создатель бота!')
    elif message.text == 'Hi' or message.text == 'hi':
        bot.reply_to(message, 'Hi again! The bot creator!')
        # Условие если человек вводит команду /rem
    elif message.text == '/rem':
        # Бот отправляет сообщение в чат, с вопросом
        bot.send_message(message.from_user.id, "Приветствую, что Вам напомнить?")
        # Бот переходит на следущий этап, функцию с нашим текстом
        bot.register_next_step_handler(message, rem_text)


# Создаем функцию в которой бот обрабатывает наше сообщение
def rem_text(message):
    # Глобально обращаемся к переменной
    global rm_text
    # Присваиваем нашей переменной, наше сообщение
    rm_text = message.text
    # Бот уточняет через сколько нам напомнить наше сообщение и переходит дальше
    bot.send_message(message.from_user.id, "Через сколько Вам напомнить?")
    bot.register_next_step_handler(message, rem_time)


# Создаем функцию, в которой работаем со временем
def rem_time(message):
    # глобально обращаемся к нашей переменной
    global rm_time
    # Создаем цикл, в котором проверяем нашу переменную на целое число
    while rm_time == 0:
        try:
            rm_time = int(message.text)
            # Выдаем ошибку, если пользователь введет текст
        except Exception:
            bot.send_message(message.from_user.id, 'Введите цифры')

    # Создаем подтекстовые кнопки
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    # Кнопка, если пользователь ввел данные правильно
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    # Кнопка, если пользователь ввел данные неправильно
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    # Создаем переменную в которой бот уточняет правильность введеных данных от пользователя
    question = 'Вам напомнить ' + rm_text + ', через ' + str(rm_time) + ' минут?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


# Создаем обработчик наших кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_keyboard(call):
    # Если пользователь нажал на кнопку да, бот отправляет наше сообщение с задержкой
    # которую указал пользователь
    if call.data == 'yes':
        # Умножаем нашу переменную с временем на 60, так как метод .sleep() принимает в себя секунды
        time.sleep(rm_time * 60)
        bot.send_message(call.message.chat.id, rm_text)
        # Если пользователь не согласен с веденными данными, повторяем вопросы по новой
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'Попробуем снова!')
        bot.send_message(call.message.chat.id, "Приветствую, что Вам напомнить?")
        bot.register_next_step_handler(call.message, rem_text)


# Запускаем нашего бота
bot.polling()
