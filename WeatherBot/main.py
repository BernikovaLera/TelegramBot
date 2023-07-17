import telebot
import requests
import json

bot = telebot.TeleBot(' ') #API telegram
API = '' #API weather service


@bot.message_handler(commands=['start'])
def start(massage):
    bot.send_message(massage.chat.id, 'Привет, рад тебя видеть! Напиши название города')


@bot.message_handler(content_types=['text'])
def get_weather(massage):
    city = massage.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(massage, f'Сейчас погода: {temp}')

        image = 'sunny.png' if temp > 5.0 else 'sun.png'
        file = open('./' + image, 'rb')
        bot.send_photo(massage.chat.id, file)
    else:
        bot.reply_to(massage, f'Город указан не верно')


bot.polling(none_stop=True)
