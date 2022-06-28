import requests
import datetime

open_weather_token = "68d9fbdfe243d7492471d889ab103968"
tg_bot_token = "5406134772:AAED9AM4k3uDyeDd7upEkX3dr6eI2VFHoR8"

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import markups as nav

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Привет {0.first_name}, напиши мне название города и я пришлю сводку погоды!'
                           .format(message.from_user), reply_markup=nav.mainMenu)


# @dp.message_handler(commands=["weather"])
# async def save_city_name(message: types.Message):
#     await bot.send_message(message.from_user.id, 'Напиши мне название города и я пришлю сводку погоды!')


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]
        feels = data["main"]["feels_like"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"Сейчас - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                            f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                            f"Ощущается как: {feels} C°\n"
                            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                            f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n"
                            f"Продолжительность дня: {length_of_the_day}\n"
                            )

    except:
        await message.reply("\U0001F914 Я не знаю такого города или проверьте название города")


@dp.message_handler(commands=["next"])
async def bot_message(message: types.Message):
    # if message.text == 'Погода':
    #     await bot.send_message(message.from_user.id, '/weather')
    if message.text == 'Прочее':
        await bot.send_message(message.from_user.id, 'Прочее', reply_markup=nav.otherMenu)
    elif message.text == 'Главное меню':
        await bot.send_message(message.from_user.id, 'Главное меню', reply_markup=nav.mainMenu)
    elif message.text == 'Информация':
        await bot.send_message(message.from_user.id, 'Информация в разработке... \U0001F468\U0000200D\U0001F4BB')
    elif message.text == 'Курс валют':
        await bot.send_message(message.from_user.id, 'Курс валют в разработке... \U0001F468\U0000200D\U0001F4BB')
    else:
        await message.reply("Неизвестная команда \U0001F937")


if __name__ == '__main__':
    executor.start_polling(dp)
