"""
telegram weather bot
"""
from __future__ import absolute_import
import os
from datetime import datetime
import telebot
import requests
import logging

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

token=os.environ.get('bottoken')
bot = telebot.TeleBot(token)



@bot.message_handler(commands=['start'])
def start(message):
    """
    func for starting
    """
    bot.send_message(message.chat.id, 'Hello! I can show you the weather today in your city. Please send me the name of the city where you would like to know the weather.')

@bot.message_handler(content_types=["text"])

def get_weather(message):
    """
    func for get weather
    """
    emoji = {
        '0':'Clear \u2600\ufe0f',
        '1':'Mainly clear \U0001f324\ufe0f',
        '2':'Partly cloudy \u26c5\ufe0f',
        '3':'overcast \u2601\ufe0f',
        '45':'Fog \U0001f32b',
        '48':'Depositing rime fog \U0001f32b',
        '51':'Drizzle: Light \U0001f327\ufe0f',
        '52':'Drizzle: moderate \U0001f327\ufe0f',
        '53':'Drizzle: dense intensity \U0001f327\ufe0f',
        '56':'Freezing Drizzle: Light \U0001f327\ufe0f',
        '57':'Freezing Drizzle: dense intensity \U0001f327\ufe0f',
        '61':'Rain: Slight \U0001f327\ufe0f',
        '63':'Rain: moderate \U0001f327\ufe0f',
        '65':'Rain: heavy intensity \U0001f327\ufe0f',
        '66':'Freezing Rain: Light \U0001f327\ufe0f',
        '67':'Freezing Rain: heavy intensity \U0001f327\ufe0f',
        '71':'Snow fall: Slight \U0001f328\ufe0f',
        '73':'Snow fall: moderate \U0001f328\ufe0f',
        '75':'Snow fall: heavy intensity \U0001f328\ufe0f',
        '77':'Snow grains \U0001f328\ufe0f',
        '80':'Rain showers: Sligh \U0001f327\ufe0f',
        '81':'Rain showers: moderate \U0001f327\ufe0f',
        '82':'Rain showers: violent \U0001f327\ufe0f',
        '85':'Snow showers slight \U0001f328\ufe0f',
        '86':'Snow showers heavy \U0001f328\ufe0f',
        '95':'Thunderstorm \U0001f300\ufe0f',
        '96':'Thunderstorm with slight and heavy hail \U0001f300\ufe0f',
        '99':'Thunderstorm with slight and heavy hail \U0001f300\ufe0f'}
    try:
        req_city=requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={message.text}")
        data_city=req_city.json()
        latitude=data_city['results'][0]['latitude']
        longitude=data_city['results'][0]['longitude']
        timezone=data_city['results'][0]['timezone']
        country=data_city['results'][0]['country']
        
        date=datetime.fromtimestamp(int(message.date))
        date_hour=int(date.hour) # get current hour

        url_string="https://api.open-meteo.com/v1/forecast?latitude=" + str(latitude) + "&longitude=" + str(longitude) + "&hourly=temperature_2m,apparent_temperature,weathercode,surface_pressure,relativehumidity_2m&daily=weathercode,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,windspeed_10m_max&current_weather=true&timezone=" + timezone
        # "https://api.open-meteo.com/v1/forecast?latitude=" + str(latitude) + "&" + "longitude="+ str(longitude) + "&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m,apparent_temperature&timezone="+timezone
        req=requests.get(url_string)
        data=req.json()
        city=message.text

        # current weather 
        cur_weather=str(data['current_weather']['temperature'])
        cur_wind=data['current_weather']['windspeed']
        cur_weather_emoji=str(data['current_weather']['weathercode'])

        if cur_weather_emoji in emoji:
            cur_weath_e=emoji[cur_weather_emoji]
        else:
            cur_weath_e='\U0001f50d\ufe0f'
        
        # daily 
        day_weather_code=str(data['daily']['weathercode'][0])
        day_wheater_min=data['daily']['temperature_2m_min'][0]
        day_wheater_max=data['daily']['temperature_2m_max'][0]
        day_feels_like_min=data['daily']['apparent_temperature_min'][0]
        day_feels_like_max=data['daily']['apparent_temperature_max'][0]
        sunrise=(str(data['daily']['sunrise'][0]))[-5:]
        sunset=(str(data['daily']['sunset'][0]))[-5:]
        day_windspeed_max=data['daily']['windspeed_10m_max'][0]

        if day_weather_code in emoji:
                day_weath_e=emoji[day_weather_code]
        else:
            day_weath_e='\U0001f50d\ufe0f'
        
        # hourly wetaher
        hourly_weather_code=str(data['hourly']['weathercode'][date_hour])
        hourly_weather=data['hourly']['temperature_2m'][date_hour]
        hourly_feels_like=data['hourly']['apparent_temperature'][date_hour]
        hourly_pressure=round((int(data['hourly']['surface_pressure'][date_hour])*0.760061),1)
        hourly_humidity=data['hourly']['relativehumidity_2m'][date_hour]
        hourly_time=(str(data['hourly']['time'][date_hour]))[-5:]

        if hourly_weather_code in emoji:
                hour_weath_e=emoji[hourly_weather_code]
        else:
            hour_weath_e='\U0001f50d\ufe0f'

        bot.send_message(message.chat.id, f'Current  weather in {city}/{country}\nCurrent temperature: {cur_weather} C° {cur_weath_e}\n'
            f'Wind speed: {cur_wind} m/s\n\n'
            f'Daily weather\nTemperature: from {day_wheater_min} C° to {day_wheater_max} C°, {day_weath_e}\n'
            f'Feels like: from {day_feels_like_min} C° to {day_feels_like_max} C°,\nWind speed: {day_windspeed_max} m/s\n'
            f'Sunrise/Sunset - {sunrise}/{sunset}\n\n'
            f'Hourly weather: {hourly_time}\nTemperature: {hourly_weather} C° {hour_weath_e}\nFeels like: {hourly_feels_like} C°\nPressure: {hourly_pressure} mm/Hg\n'
            f'Humidity: {hourly_humidity} %')
    except Exception:
        bot.send_message(message.chat.id, "I can't find this city. Try again.")



bot.polling(none_stop=True, interval=0)
