import telebot
from currency_converter import CurrencyConverter
from telebot import types



bot = telebot.TeleBot('6052984577:AAEZBfxOVyH9YJPgmJaS_1jNM98kLgrxS3M')
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму')
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Введите сумму.')
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('RUB/USD', callback_data='rub/usd')
        # btn2 = types.InlineKeyboardButton('USD/RUB', callback_data='usd/rub')
        btn3 = types.InlineKeyboardButton('RUB/EUR', callback_data='rub/eur')
        # btn4 = types.InlineKeyboardButton('EUR/RUB', callback_data='eur/rub')
        btn5 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn6 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn7 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn3, btn5, btn6, btn7)
        bot.send_message(message.chat.id, 'Выберете пару валют, через слеш', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Неверный формат. Введите сумму.')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму.')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, f'Введите пару значений через слеш')
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    try:
        values = message.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму.')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Неверный формат. Впишите значение заново.')
        bot.register_next_step_handler(message, my_currency)


bot.polling(none_stop=True)
