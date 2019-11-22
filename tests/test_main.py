import pytest
import requests
import requests_mock
import main

url = "https://api.openweathermap.org"
data_url = f"{url}/data/2.5/weather"


def test_get_weather_data(requests_mock):
    requests_mock.get(data_url, json="test")
    response = main.get_weather_data(data_url)
    assert response == "test"