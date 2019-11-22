import requests
from typing import Mapping, Any

KEY = "165c09ec420c7f790349861c6d6309d2"
LAT = "51.52"
LON = "0.4"
PARAMS = f"?lat={LAT}&lon={LON}&APPID={KEY}&units=metric"
URL = "https://api.openweathermap.org"
DATA_ENDPOINT = f"{URL}/data/2.5/weather{PARAMS}"
FORCAST_ENDPOINT = f"{URL}/data/2.5/forecast{PARAMS}"


def get_weather_data(url: str) -> Mapping[str, Any]:
    response = requests.get(url)
    data = response.json()
    return data


def get_weather():
    data = get_weather_data(DATA_ENDPOINT)
    # print(data)

    temp = data["main"]["temp"]
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    temp_max = data["main"]["temp_max"]
    temp_min = data["main"]["temp_min"]

    print(f"Temp: {temp}°C, Pressure: {pressure} hpa, Humidity: {humidity}%\n")


def get_forcast():
    forcast_data = get_weather_data(FORCAST_ENDPOINT)["list"]
    # print(forcast_data)

    prediction_data = sorted(forcast_data, key=lambda k: int(k['dt'])) 

    for prediction in forcast_data:
        temp = prediction["main"]["temp"]
        pressure = prediction["main"]["pressure"]
        humidity = prediction["main"]["humidity"]
        temp_max = prediction["main"]["temp_max"]
        temp_min = prediction["main"]["temp_min"]
        print(f"Temp: {temp}°C, Pressure: {pressure} hpa, Humidity: {humidity}%")



def main():
    get_weather()
    get_forcast()


if __name__ == "__main__":
    main()
