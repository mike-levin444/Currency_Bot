import telebot
from config import API_TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    text = "Чтобы узнать цену валюты, отправьте сообщение в формате:\n<имя валюты цену которой вы хотите узнать> " \
           "<имя валюты в которой надо узнать цену первой валюты> <количество первой валюты>\n" \
           "Для просмотра всех доступных валют отправьте команду: /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def handle_values(message):
    text = "Доступные валюты: USD, EUR, RUB"
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def handle_convert(message):
    try:
        base, quote, amount = message.text.split(' ')

        result = CurrencyConverter.get_price(base.upper(), quote.upper(), amount)
        text = f"Цена {amount} {base} в {quote} = {result}"
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка пользователя: {str(e)}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Не удалось обработать команду: {str(e)}")
    else:
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)