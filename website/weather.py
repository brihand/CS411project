import json
import requests
import config

# Weather App Id
WEATHER_APP_ID = config.WEATHER_APP_ID

# OpenWeatherMap URLS
WEATHER_API_BASE_URL = "http://api.openweathermap.org/data"
WEATHER_API_VERSION = "2.5"
WEATHER_API_URL = "{}/{}/weather".format(WEATHER_API_BASE_URL, WEATHER_API_VERSION)

def getWeatherFromZip(zipcode):
    """ Through a US zipcode, gets the json for the weather """
    state = 'us'
    weather_api_endpoint = "{}?zip={},{}&appid={}".format(WEATHER_API_URL,zipcode,state,WEATHER_APP_ID)
    weather_response = requests.get(weather_api_endpoint)
    weather_data = json.loads(weather_response.text)

    return weather_data