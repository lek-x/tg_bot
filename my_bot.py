"""
my tg bot
"""
from __future__ import absolute_import
import os
import datetime
import telebot
import requests
token=os.environ.get('bottoken')
weathertok=os.environ.get('weathertok')
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    """
    func for starting
    """
    bot.send_message(message.chat.id, 'Hello! I can show you the weather today in your city.\
    Please send me the name of the city\
    where you would like to know the weather.')

@bot.message_handler(content_types=["text"])
def get_weather(message):
    """
    func for get weather
    """
    emoji = {
        'Clear': 'Clear \u2600\ufe0f',
        'Clouds':'Clouds \u2601\ufe0f',
        'Rain':'Rain \U0001f327\ufe0f',
        'Drizzle':'Drizzle \U0001f327\ufe0f',
        'Thunderstorm':'Thunderstorm \u26c8\ufe0f',
        'Snow':'Snow \U0001f328\ufe0f',
        'Mist':'Mist \U0001f32b',
        'Fog':'Fog \U0001f32b'}
    try:

        req=requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weathertok}&units=metric")
        data=req.json()
        city=data['name']
        cur_weather=int(data['main']['temp'])
        weather_emoji=data['weather'][0]['main']
        if weather_emoji in emoji:
            weath_e=emoji[weather_emoji]
        else:
            weath_e='\U0001f327\ufe0f'
        feels_like=int(data['main']['feels_like'])
        humidity=data['main']['humidity']
        pressure=int(data['main']['pressure']/ 1.333)
        wind=data['wind']['speed']
        sunrise=datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset=datetime.datetime.fromtimestamp(data['sys']['sunset'])
        bot.send_message(message.chat.id, f'The weather in {city}\n\
            Current temperature: {cur_weather}C°\
             {weath_e}\nFeels like: {feels_like}C°\n'
            f'Humidity: {humidity}%\nPressure: {pressure}mmHg\nWind:\
             {wind}m/s\nSunrise: {sunrise}\nSunset: {sunset}'
        )
    except Exception:
        bot.send_message(message.chat.id, "I can't find this city. Try again.")



bot.polling(none_stop=True, interval=0)
