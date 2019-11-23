import json
import pytest
import requests
import main

base_url = "https://api.openweathermap.org"
data_url = f"{base_url}/data/2.5/weather"
forcast_url = f"{base_url}/data/2.5/forecast"


def test_call_api(requests_mock):
    requests_mock.get(data_url, json="test")
    response = main.call_api(data_url)
    assert response == "test"


def test_weather_reading_to_json():
    weather = main.WeatherReading(1, 2, 3, 4, 5, 6)
    assert weather.temp == 1
    assert weather.pressure == 2
    assert weather.humidity == 3
    assert weather.temp_min == 4
    assert weather.temp_max == 5
    assert weather.datetime == 6


def test_extract_weather():
    data = {
        "main": {
            "temp": "temp",
            "pressure": "pressure",
            "humidity": "humidity",
            "temp_max": "temp_max",
            "temp_min": "temp_min",
        },
        "dt": "dt",
    }
    weather = main.extract_weather(data)
    assert weather.temp == "temp"
    assert weather.pressure == "pressure"
    assert weather.humidity == "humidity"
    assert weather.temp_max == "temp_max"
    assert weather.temp_min == "temp_min"
    assert weather.datetime == "dt"


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


def test_get_forcast(requests_mock):
    with open('./tests/data/forcast_data.json') as json_file:
        data = json.load(json_file)
        requests_mock.get(forcast_url, json=data)
    forcast = main.get_forcast()
    assert len(forcast) == 40
    # assert isinstance(forcast, main.WeatherReading)
    assert forcast[0].temp == 8.32
    assert forcast[0].pressure == 994
    assert forcast[0].humidity == 80
    assert forcast[0].temp_max == 9.32
    assert forcast[0].temp_min == 8.32
    assert forcast[0].datetime == 1574467200
