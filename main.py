import requests
from dataclasses import dataclass
from typing import Mapping, Any

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

    def print_weather(self):
        print(f"Temp: {self.temp}°C")
        print(f"Pressure: {self.pressure}hpa")
        print(f"Humidity: {self.humidity}%")
        print(f"Max Temp: {self.temp_max}°C")
        print(f"min Temp: {self.temp_min}°C")
        print("")


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


def get_weather():
    data = call_api(DATA_ENDPOINT)
    weather = extract_weather(data)
    weather.print_weather()


def get_forcast():
    forcast_data = call_api(FORCAST_ENDPOINT)["list"]
    forcast_data = sorted(forcast_data, key=lambda k: int(k['dt']))
    forcast_weather = [extract_weather(i) for i in forcast_data]

    for prediction in forcast_weather:
        prediction.print_weather()


def main():
    get_weather()
    get_forcast()


if __name__ == "__main__":
    main()
