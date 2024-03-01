from config import TOKEN, open_wheather_token
import telebot
import requests
import datetime

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def say_hello(message):
    bot.send_message(message.chat.id, 'Привет ! Я робот - помощник. Я расскажу тебе всё о погоде в любом городе ! '
                                      'Чтобы получить список доступных команд введи /help')


@bot.message_handler(commands=['help'])
def list_of_commands(message):
    commands_list = ('Вот список доступных команд:\n'
                     '/start - начать работу\n'
                     '/common_information - выводит всю информацию о заданном городе\n'
                     '/help - выводит список доступных команд'

                     )
    bot.send_message(message.chat.id, commands_list)


@bot.message_handler(commands=['common_information'])
def request_result(message):
    bot.reply_to(message, 'Введите город: ')


def get_wheather(city, token):
    code_wheather = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U0001F327",
        "Drizzle": "Морось \U0001F326",
        "Thunderstorm": "Гроза \U000026C8",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B",
    }
    try:
        my_req = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}&units=metric&lang=ru'
        )
        data = my_req.json()
        city = data['name']
        curr_wheather = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']

        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])
        wheather_description = data['weather'][0]['main']

        response = f"Город: {city}\n" \
                   f"Текущая температура: {curr_wheather} °C\n{code_wheather[wheather_description]}\n" \
                   f"Влажность: {humidity} %\n" \
                   f"Давление: {pressure} hPa\n" \
                   f"Скорость ветра: {wind} м/с\n" \
                   f"Восход солнца: {sunrise}\n" \
                   f"Закат солнца: {sunset}\n" \
                   f"Длительность дня: {length_of_the_day}\n"

        return response

    except requests.exceptions.HTTPError as http_err:
        return f"Ошибка при запросе к серверу погоды: {http_err}"
    except KeyError:
        return "Город не найден. Пожалуйста, введите корректное название города."
    except Exception as ex:
        return f"Ошибка: {ex}"


@bot.message_handler()
def process_city(message):
    bot.reply_to(message, get_wheather(message.text, open_wheather_token))


if __name__ == '__main__':
    bot.infinity_polling()
