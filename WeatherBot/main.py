import telebot
import requests
import json
import datetime
import math


bot = telebot.TeleBot('6052984577:AAEZBfxOVyH9YJPgmJaS_1jNM98kLgrxS3M')
API = '88a4cc29f0c4a016373a14a6b45e757f'


@bot.message_handler(commands=['start'])
def start(massage):
    bot.send_message(massage.chat.id, 'Привет, рад тебя видеть! Напиши название города')


@bot.message_handler(content_types=['text'])
def get_weather(massage):
    city = massage.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&lang=ru&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = round(data["main"]["temp"], 0)
        description = data['weather'][0]['description']
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        bot.reply_to(massage, f'Температура воздуха сейчас {temp} C°\n'
                              f'Погода: {description}\n'
                              f'Влажность: {humidity}%\n'
                              f'Давление: {math.ceil(pressure/1.333)} мм.рт.ст\n'
                              f'Ветер: {wind} м/с \n'
                              f'Восход солнца: {sunrise_timestamp}\n'
                              f'Закат солнца: {sunset_timestamp}\n'
                              f'Продолжительность дня: {length_of_the_day}\n')


        # image = 'sunny.png' if temp > 5.0 else 'sun.png'
        # file = open('./' + image, 'rb')
        # bot.send_photo(massage.chat.id, file)
    else:
        bot.reply_to(massage, f'Город указан не верно')


bot.polling(none_stop=True)
