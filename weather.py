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
if not (KEY and LAT and LON):
    raise Exception("Missing env vars!")


API_CACHE_TTL = 1 * 60
PARAMS = f"?lat={LAT}&lon={LON}&APPID={KEY}&units=metric"
BASE_URL = "https://api.openweathermap.org"
DATA_ENDPOINT = f"{BASE_URL}/data/2.5/weather{PARAMS}"
FORCAST_ENDPOINT = f"{BASE_URL}/data/2.5/forecast{PARAMS}"


@dataclass
class WeatherReading:
    temp: float
    humidity: int
    pressure: int = 0
    temp_min: float = 0.0
    temp_max: float = 0.0
    datetime: int = 0
    wind_speed: int = 0.0
    wind_direction: str = "N/A"
    description: str = ""
    img_id: str = ""

    def __post_init__(self):
        self.datetime = self.date_to_str(self.datetime)
        self.wind_direction = self.get_cardinal_direction(self.wind_direction)

    def to_json(self):
        return {k: v for (k, v) in vars(self).items()}

    def date_to_str(self, epoch):
        dt = datetime.datetime.fromtimestamp(epoch)
        return dt.strftime("%Y-%m-%d %H:%M")

    def get_cardinal_direction(self, angle):
        dirs = [
            'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
            'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        ix = round(angle / (360. / len(dirs)))
        return dirs[ix % len(dirs)]


def call_api(url: str) -> Mapping[str, Any]:
    response = requests.get(url)
    log.debug("Api status code: %s", response.status_code)
    log.debug("Raw api response: %s", response)

    if response.status_code != 200:
        log.error("Invalid api response")

        if response.status_code == 429:
            log.error("Api limit reached for free teir - 60 calls per min.")

        if response.status_code == 404:
            log.error("Invalid url parameters.")

        if response.status_code == 401:
            log.error("Invalid api key.")

        raise Exception(response.text)

    data = response.json()
    return data


def extract_weather(data: Mapping[str, Any]) -> WeatherReading:
    wind_direction = "N/A"
    if "deg" in data["wind"]:
        wind_direction = data["wind"]["deg"]

    return WeatherReading(
        temp=data["main"]["temp"],
        pressure=data["main"]["pressure"],
        humidity=data["main"]["humidity"],
        temp_max=data["main"]["temp_max"],
        temp_min=data["main"]["temp_min"],
        datetime=data["dt"],
        wind_speed=data["wind"]["speed"],
        wind_direction=wind_direction,
        description=data["weather"][0]["description"],
        img_id=data["weather"][0]["icon"],
    )


@cachetools.func.ttl_cache(ttl=API_CACHE_TTL)
def get_weather() -> WeatherReading:
    log.info("Getting current weather")
    data = call_api(DATA_ENDPOINT)
    data["dt"] = datetime.datetime.now().timestamp()
    log.debug("Raw current weather: %s", data)
    weather = extract_weather(data)
    return weather


@cachetools.func.ttl_cache(ttl=API_CACHE_TTL)
def get_forcast() -> List[WeatherReading]:
    log.info("Getting forcast weather")
    forcast_data = call_api(FORCAST_ENDPOINT)["list"]
    log.debug("Raw forcast data: %s", forcast_data)
    forcast_data = sorted(forcast_data, key=lambda k: int(k['dt']))
    forcast_weather = [extract_weather(i) for i in forcast_data]
    return forcast_weather


def get_indoors():
    log.info("Getting indoors weather")

    if os.environ.get("RPI") == "True":
        from smbus import SMBus
        from bmp280 import BMP280
        bus = SMBus(1)
        bmp280 = BMP280(i2c_dev=bus)
        bmp280.setup(mode="forced")
        temperature = bmp280.get_temperature()
        pressure = bmp280.get_pressure()

    else:
        temperature = 0.0
        pressure = 0.0

    log.debug("Raw indoors weather: {:05.2f}*C {:05.2f}hPa".format(temperature, pressure))

    # return WeatherReading(temperature, pressure)
    return {
        "temp": round(temperature, 2),
        "pressure": round(pressure, 2),
    }
