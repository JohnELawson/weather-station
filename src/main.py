import datetime
import requests
import cachetools.func
from dataclasses import dataclass
from typing import Mapping, Any, List
from flask_api import FlaskAPI

KEY = "165c09ec420c7f790349861c6d6309d2"
LAT = "51.52"
LON = "0.4"
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
    
    def to_json(self):
        return {
            "temp": self.temp,
            "pressure": self.pressure,
            "humidity": self.humidity,
            "temp_max": self.temp_max,
            "temp_min": self.temp_min,
            "datetime": self.get_nice_date,
        }

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
        datetime=data["dt"]
    )


@cachetools.func.ttl_cache(ttl=1 * 60)
def get_weather() -> WeatherReading:
    data = call_api(DATA_ENDPOINT)
    data["dt"] = datetime.datetime.now().timestamp()
    weather = extract_weather(data)
    # weather.print_weather()
    return weather


@cachetools.func.ttl_cache(ttl=1 * 60)
def get_forcast() -> List[WeatherReading]:
    forcast_data = call_api(FORCAST_ENDPOINT)["list"]
    forcast_data = sorted(forcast_data, key=lambda k: int(k['dt']))
    forcast_weather = [extract_weather(i) for i in forcast_data]
    # for prediction in forcast_weather:
    #     prediction.print_weather()
    return forcast_weather


app = FlaskAPI(__name__)


@app.route('/current_weather/')
def get_current_weather():
    return get_weather().to_json()


@app.route('/forcast_weather/')
def get_forcast_weather():
    return { i: forcast.to_json() for i, forcast in enumerate(get_forcast()) }


if __name__ == "__main__":
   app.run(debug=True)
