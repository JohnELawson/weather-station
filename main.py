import requests
from dataclasses import dataclass
from typing import Mapping, Any

KEY = "165c09ec420c7f790349861c6d6309d2"
# KEY = "b1b15e88fa797225412429c1c50c122a1"
LAT = "51.52"
LON = "0.4"
PARAMS = f"?lat={LAT}&lon={LON}&APPID={KEY}&units=metric"
BASIC_URL = "https://api.openweathermap.org"
PRO_URL = "https://pro.openweathermap.org"
DATA_ENDPOINT = f"{BASIC_URL}/data/2.5/weather{PARAMS}"
FORCAST_ENDPOINT = f"{BASIC_URL}/data/2.5/forecast{PARAMS}"
# HOURLY_FORCAST_ENDPOINT = f"https://pro.openweathermap.org/data/2.5/forecast/hourly{PARAMS}"


@dataclass
class WeatherReading:
    temp: float
    pressure: int
    humidity: int
    temp_min: float
    temp_max: float


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
    )


def print_weather(weather: WeatherReading) -> None:
    print(f"Temp: {weather.temp}°C")
    print(f"Pressure: {weather.pressure}hpa")
    print(f"Humidity: {weather.humidity}%")
    print(f"Max Temp: {weather.temp_max}°C")
    print(f"min Temp: {weather.temp_min}°C")
    print("")


def get_weather():
    data = call_api(DATA_ENDPOINT)
    weather = extract_weather(data)
    print_weather(weather)


def get_forcast():
    forcast_data = call_api(FORCAST_ENDPOINT)["list"]
    prediction_data = sorted(forcast_data, key=lambda k: int(k['dt'])) 
    for prediction in forcast_data:
        weather = extract_weather(prediction)
        print_weather(weather)


def main():
    get_weather()
    get_forcast()


if __name__ == "__main__":
    main()
