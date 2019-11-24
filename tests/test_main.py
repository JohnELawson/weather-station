import main
from .test_weather import mock_forcast, mock_weather


def test_get_current_weather_api(requests_mock):
    mock_weather(requests_mock)
    response = main.get_current_weather()
    assert response["temp"] == 7.71
    assert response["pressure"] == 995
    assert response["humidity"] == 93
    assert response["temp_max"] == 9.44
    assert response["temp_min"] == 6.67
    assert response["wind_direction"] == "E"
    assert response["wind_speed"] == 5.1


def test_get_forcast_weather_api(requests_mock):
    mock_forcast(requests_mock)
    response = main.get_forcast_weather()
    assert len(response) == 40
    assert response[0]["temp"] == 8.32
    assert response[0]["pressure"] == 994
    assert response[0]["humidity"] == 80
    assert response[0]["temp_max"] == 9.32
    assert response[0]["temp_min"] == 8.32
    assert response[0]["datetime"] == '2019-11-23 00:00'
    assert response[0]["wind_speed"] == 9.11
    assert response[0]["wind_direction"] == "SE"
