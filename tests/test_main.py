import json
import pytest
import requests
import main

url = "https://api.openweathermap.org"
data_url = f"{url}/data/2.5/weather"


def test_call_api(requests_mock):
    requests_mock.get(data_url, json="test")
    response = main.call_api(data_url)
    assert response == "test"


def test_extract_weather():
    data = {
        "main": {
            "temp": "temp",
            "pressure": "pressure",
            "humidity": "humidity",
            "temp_max": "temp_max",
            "temp_min": "temp_min",
        }
    }
    weather = main.extract_weather(data)
    assert weather.temp == "temp"
    assert weather.pressure == "pressure"
    assert weather.humidity == "humidity"
    assert weather.temp_max == "temp_max"
    assert weather.temp_min == "temp_min"


def test_get_weather(requests_mock):
    with open('./tests/data/weather_data.json') as json_file:
        data = json.load(json_file)
        requests_mock.get(data_url, json=data)
    weather = main.get_weather()
    assert weather.temp == 7.71
    assert weather.pressure == 995
    assert weather.humidity == 93
    assert weather.temp_max == 9.44
    assert weather.temp_min == 6.67
