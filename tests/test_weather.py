import json
import pytest
import weather

base_url = "https://api.openweathermap.org"
data_url = f"{base_url}/data/2.5/weather"
forcast_url = f"{base_url}/data/2.5/forecast"


@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):
    monkeypatch.setenv("LON", "111")
    monkeypatch.setenv("LAT", "222")
    monkeypatch.setenv("WEATHER_API_KEY", "333")


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
    response = weather.call_api(data_url)
    assert response == "test"


def test_weather_reading_to_json():
    response = weather.WeatherReading(1, 2, 3, 4, 5, 6, 7, 8).to_json()
    assert response["humidity"] == 2
    assert response["pressure"] == 3
    assert response["temp_min"] == 4
    assert response["temp_max"] == 5
    assert response["datetime"] == '1970-01-01 01:00'
    assert response["wind_speed"] == 7
    assert response["wind_direction"] == "N"


def test_get_nice_wind_direction():
    data = {
        "N": 2,
        "NE": 45,
        "S": 180,
        "W": 270
    }
    for direction, angle in data.items():
        assert weather.WeatherReading(
            1, 2, 3, 4, 5, 6, 7,
            wind_direction=angle
        ).wind_direction == direction


def test_extract_weather():
    data = {
        "main": {
            "temp": "temp",
            "pressure": "pressure",
            "humidity": "humidity",
            "temp_max": "temp_max",
            "temp_min": "temp_min",
        },
        "dt": 1,
        "wind": {
            "speed": "wind_speed",
            "deg": 100,
        },
        "weather": [
            {
                "id": 804,
                "main": "Clouds",
                "description": "overcast clouds",
                "icon": "04n"
            }
        ],
    }
    response = weather.extract_weather(data)
    assert response.temp == "temp"
    assert response.pressure == "pressure"
    assert response.humidity == "humidity"
    assert response.temp_max == "temp_max"
    assert response.temp_min == "temp_min"
    assert response.datetime == '1970-01-01 01:00'
    assert response.wind_speed == "wind_speed"
    assert response.wind_direction == "E"


def test_get_weather(requests_mock):
    mock_weather(requests_mock)
    response = weather.get_weather()
    assert response.temp == 7.71
    assert response.pressure == 995
    assert response.humidity == 93
    assert response.temp_max == 9.44
    assert response.temp_min == 6.67
    assert response.wind_direction == "E"
    assert response.wind_speed == 5.1


def test_get_forcast(requests_mock):
    mock_forcast(requests_mock)
    forcast = weather.get_forcast()
    assert len(forcast) == 40
    # assert isinstance(forcast, weather.WeatherReading)
    assert forcast[0].temp == 8.32
    assert forcast[0].pressure == 994
    assert forcast[0].humidity == 80
    assert forcast[0].temp_max == 9.32
    assert forcast[0].temp_min == 8.32
    assert forcast[0].datetime == '2019-11-23 00:00'
    assert forcast[0].wind_speed == 9.11
    assert forcast[0].wind_direction == "SE"
