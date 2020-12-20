import json
import requests
import sqlite3
import time
import datetime
import schedule
from flask import jsonify


class Weather(object):
    def __init__(self):
        self.__headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.wikipedia.org/',
            'Connection': 'keep-alive',
        }

    def __get_lat_lon(self,zipcode='06604'):

        """
        This is Private class Client dont have Access to this
        :param zipcode: Takes Zip Code
        :return: Lat and Long
        """
        self.__url_zip = 'https://api.promaptools.com/service/us/zip-lat-lng/get/'

        params = {
            'key': '17o8dysaCDrgv1c',
            'zip':zipcode
        }

        r = requests.get(url=self.__url_zip,headers=self.__headers,params=params)
        data = r.json()

        for x in data["output"]:
            return x["latitude"], x["longitude"]

    def weather_get(self,zip='06604'):
        """
        :param zip: Takes Zip code as String
        :return: Weather Information
        """

        lat, long = self.__get_lat_lon(zip)

        data = '{},{}'.format(lat,long)

        self.__url_weather = "https://api.weather.com/v2/turbo/vt1observation"

        params= {
            'apiKey': 'd522aa97197fd864d36b418f39ebb323',
            'format': 'json',
            'geocode': data,
            'language': 'en-US',
            'units':'e'
        }

        r2 = requests.get(url=self.__url_weather,headers=self.__headers,params=params)

        r2_data = r2.json()
        print(r2_data)



        dew_point = r2_data["vt1observation"]["dewPoint"]
        feelsLike = r2_data["vt1observation"]["feelsLike"]
        humidity = r2_data["vt1observation"]["humidity"]
        observationTime = r2_data["vt1observation"]["observationTime"]
        temperature = r2_data["vt1observation"]["temperature"]
        visibility = r2_data["vt1observation"]["visibility"]

        windspeed = r2_data["vt1observation"]["windSpeed"]
        winddegree = r2_data["vt1observation"]["windDirDegrees"]
        winddirection = r2_data["vt1observation"]["windDirCompass"]

        phrase = r2_data["vt1observation"]['phrase']
        uvindex = r2_data["vt1observation"]['uvIndex']

        return r2_data
    
    
    def the_weather_get(self,name='Ho Chi Minh'):
        """
        :param name: Takes name as String
        :return: Weather Information
        """

        self.__url_weather = "https://community-open-weather-map.p.rapidapi.com/weather"
        self.__headers = {
            'x-rapidapi-key': "6e3b89e9d1msh988c7168dd3cc7fp1c8177jsn96c9c26a0d5b",
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
        }

        params= {
            "q": name,
            "lat":"0",
            "lon":"0",
            "callback":"test",
            "id":"2172797",
            "lang":"null",
            "units":"\"metric\" or \"imperial\"",
            "mode":"xml, html"
        }
        

        r2 = requests.get(url=self.__url_weather,headers=self.__headers,params=params)

        r2_data = json.loads(r2.text[5:-1])
        print(r2_data)

        city_name = r2_data["name"]+ ' - ' + r2_data["sys"]["country"]
        feelsLike = r2_data["main"]["feels_like"]
        humidity = r2_data["main"]["humidity"]
        temp = r2_data["main"]["temp"]
        temp_min = r2_data["main"]["temp_min"]
        temp_max = r2_data["main"]["temp_max"]
        visibility = r2_data["visibility"]

        windspeed = r2_data["wind"]["speed"]
        winddegree = r2_data["wind"]["deg"]
        description = r2_data["weather"][0]["description"]
        icon = "http://openweathermap.org/img/w/" + r2_data["weather"][0]["icon"] + ".png"
        
        data = {
            "city_name": city_name,
            "feelsLike": feelsLike,
            "humidity": humidity,
            "temp": temp,
            "temp_min": temp_min,
            "temp_max": temp_max,
            "visibility": visibility,
            "windspeed": windspeed,
            "winddegree": winddegree,
            "description": description,
            "icon": icon
        }

        return r2_data


w = Weather()
data = w.the_weather_get(name='Ho Chi Minh')
