import os

import requests
from dotenv import load_dotenv

from utility import SMILE

load_dotenv()


chat_id = os.getenv('CHAT_ID')
KEY = os.getenv('KEY')
URL = 'http://api.weatherapi.com/v1/forecast.json?key='

dict_wind = {'N': 'северный', 'S': 'южный', 'E': 'восточный', 'W': 'западный',
             'NE': 'северо-востоный', 'SE': 'юго-востоный',
             'NW': 'северо-западный', 'SW': 'юго-западный'}

dict_city = {'Egvekinot': 'Эгвекиноте', 'Amguema': 'Амгуэме'}


def get_weater(city):
    new_url = URL + KEY + '&q=' + city + '&lang=ru&days=3&aqi=no&alerts=no'
    response = requests.get(new_url)
    return response.json()


def set_responce(city, n):
    time = get_weater(city)["forecast"]["forecastday"][n]["hour"][9]["time"]
    location = get_weater(city)["location"]
    city = location["name"]
    temp = get_weater(city)["forecast"]["forecastday"][n]["hour"][9]["temp_c"]
    text = get_weater(city)["forecast"]["forecastday"][n]["hour"][9]["condition"]["text"]
    wind = round(get_weater(city)["forecast"]["forecastday"][n]["hour"][9]["wind_kph"] * 1000 / 3600, 1)
    wind_dir = dict_wind.get(get_weater(city)["forecast"]["forecastday"][n]["hour"][9]["wind_dir"])
    pressure = get_weater(city)["forecast"]["forecastday"][n]["hour"][9]["pressure_mb"] * 0.75
    precip = get_weater(city)["forecast"]["forecastday"][n]["hour"][9]["precip_mm"]
    humidity = get_weater(city)["forecast"]["forecastday"][n]["hour"][9]["humidity"]
    cloud = get_weater(city)["forecast"]["forecastday"][n]["hour"][9]["cloud"]
    feelslike = get_weater(city)["forecast"]["forecastday"][n]["hour"][9]["feelslike_c"]
    vis = get_weater(city)["forecast"]["forecastday"][n]["hour"][9]["vis_km"]
    return (f'{time} в {dict_city.get(city)} {text.lower()}'
            f'\n{SMILE[0]}температура {temp} градусов по цельсию'
            f'\n{SMILE[1]}ощущается как {feelslike} градусов по цельсию'
            f'\n{SMILE[2]}ветер {wind_dir} {wind} м/с'
            f'\n{SMILE[3]}давление {pressure} мм/рт.ст.'
            f'\n{SMILE[4]}осадки {precip} мм'
            f'\n{SMILE[5]}влажность {humidity}%'
            f'\n{SMILE[6]}облачность {cloud}%'
            f'\n{SMILE[7]}видимость {vis} км')

def new_weather(update, context):
    city = update.message.text.replace('/', '')
    chat = update.effective_chat
    for n in range(0, 3):
        context.bot.send_message(chat.id, set_responce(city, n))
