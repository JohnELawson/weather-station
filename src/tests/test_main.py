import json
import pytest
import requests
import main

base_url = "https://api.openweathermap.org"
data_url = f"{base_url}/data/2.5/weather"
forcast_url = f"{base_url}/data/2.5/forecast"


def mock_weather(requests_mock):
    with open('./tests/data/weather_data.json') as json_file:
        data = json.load(json_file)
        requests_mock.get(data_url, json=data)

    
def mock_forcast(requests_mock):
    with open('./tests/data/forcast_data.json') as json_file:
        data = json.load(json_file)
        requests_mock.get(forcast_url, json=data)


def test_call_api(requests_mock):
    requests_mock.get(data_url, json="test")
    response = main.call_api(data_url)
    assert response == "test"


def test_weather_reading_to_json():
    weather = main.WeatherReading(1, 2, 3, 4, 5, 6, 7, 8).to_json()
    assert weather["pressure"] == 2
    assert weather["humidity"] == 3
    assert weather["temp_min"] == 4
    assert weather["temp_max"] == 5
    assert weather["datetime"] == '1970-01-01 01:00'
    assert weather["wind_speed"] == 7
    assert weather["wind_angle"] == 8

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
        "wind": {
            "speed": "wind_speed",
            "deg": "wind_angle"
        }
    }
    weather = main.extract_weather(data)
    assert weather.temp == "temp"
    assert weather.pressure == "pressure"
    assert weather.humidity == "humidity"
    assert weather.temp_max == "temp_max"
    assert weather.temp_min == "temp_min"
    assert weather.datetime == "dt"
    assert weather.wind_speed == "wind_speed"
    assert weather.wind_angle == "wind_angle"


def test_get_weather(requests_mock):
    mock_weather(requests_mock)
    weather = main.get_weather()
    assert weather.temp == 7.71
    assert weather.pressure == 995
    assert weather.humidity == 93
    assert weather.temp_max == 9.44
    assert weather.temp_min == 6.67
    assert weather.wind_angle == 100
    assert weather.wind_speed == 5.1


def test_get_current_weather_api():
    response = main.get_current_weather()
    assert response["temp"] == 7.71
    assert response["pressure"] == 995
    assert response["humidity"] == 93
    assert response["temp_max"] == 9.44
    assert response["temp_min"] == 6.67
    assert response["wind_angle"] == 100
    assert response["wind_speed"] == 5.1


def test_get_forcast(requests_mock):
    mock_forcast(requests_mock)
    forcast = main.get_forcast()
    assert len(forcast) == 40
    # assert isinstance(forcast, main.WeatherReading)
    assert forcast[0].temp == 8.32
    assert forcast[0].pressure == 994
    assert forcast[0].humidity == 80
    assert forcast[0].temp_max == 9.32
    assert forcast[0].temp_min == 8.32
    assert forcast[0].datetime == 1574467200
    assert forcast[0].wind_speed == 9.11
    assert forcast[0].wind_angle == 124


def test_get_current_weather_api():
    response = main.get_forcast_weather()
    assert len(response) == 40
    assert response[0]["temp"] == 8.32
    assert response[0]["pressure"] == 994
    assert response[0]["humidity"] == 80
    assert response[0]["temp_max"] == 9.32
    assert response[0]["temp_min"] == 8.32
    assert response[0]["datetime"] == '2019-11-23 00:00'
    assert response[0]["wind_speed"] == 9.11
    assert response[0]["wind_angle"] == 124
