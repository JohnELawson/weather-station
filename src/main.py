import logging
from flask_api import FlaskAPI
from weather import get_weather, get_forcast

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

app = FlaskAPI(__name__)

@app.route('/current_weather/')
def get_current_weather():
    return get_weather().to_json()


@app.route('/forcast_weather/')
def get_forcast_weather():
    return [ i.to_json() for i in get_forcast() ]


if __name__ == "__main__":
   app.run(debug=True)
