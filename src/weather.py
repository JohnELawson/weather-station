import os
import logging
import datetime
import requests
import cachetools.func
from dataclasses import dataclass
from typing import Mapping, Any, List


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


KEY = os.environ.get("WEATHER_API_KEY")
LAT = os.environ.get("LAT") 
LON = os.environ.get("LON") 
PARAMS = f"?lat={LAT}&lon={LON}&APPID={KEY}&units=metric"
BASE_URL = "https://api.openweathermap.org"
DATA_ENDPOINT = f"{BASE_URL}/data/2.5/weather{PARAMS}"
FORCAST_ENDPOINT = f"{BASE_URL}/data/2.5/forecast{PARAMS}"


@dataclass
class WeatherReading:
    temp: float
    pressure: int
    humidity: int
    temp_min: float
    temp_max: float
    datetime: int
    wind_speed: int
    wind_angle: int
    

    def to_json(self):
        self.datetime = self.get_nice_date()
        return { k:v for (k, v) in vars(self).items() }


    def get_nice_date(self):
        dt = datetime.datetime.fromtimestamp(self.datetime)
        return dt.strftime("%Y-%m-%d %H:%M")


def call_api(url: str) -> Mapping[str, Any]:
    response = requests.get(url)
    data = response.json()
    return data


def extract_weather(data: Mapping[str, Any]) -> WeatherReading:
    return WeatherReading(
        temp=data["main"]["temp"],
        pressure=data["main"]["pressure"],
        humidity=data["main"]["humidity"],
        temp_max=data["main"]["temp_max"],
        temp_min=data["main"]["temp_min"],
        datetime=data["dt"],
        wind_speed=data["wind"]["speed"],
        wind_angle=data["wind"]["deg"],
    )


@cachetools.func.ttl_cache(ttl=1 * 60)
def get_weather() -> WeatherReading:
    data = call_api(DATA_ENDPOINT)
    data["dt"] = datetime.datetime.now().timestamp()
    weather = extract_weather(data)
    return weather


@cachetools.func.ttl_cache(ttl=1 * 60)
def get_forcast() -> List[WeatherReading]:
    forcast_data = call_api(FORCAST_ENDPOINT)["list"]
    forcast_data = sorted(forcast_data, key=lambda k: int(k['dt']))
    forcast_weather = [extract_weather(i) for i in forcast_data]
    return forcast_weather
