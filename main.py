import logging
from flask import Flask, render_template
from flask_cors import CORS

import bmc280.bmc280 as bmc280
from weather import get_weather, get_forcast

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')
CORS(app)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/current_weather/')
def get_current_weather():
    return get_weather().to_json()


@app.route('/forcast_weather/')
def get_forcast_weather():
    return [i.to_json() for i in get_forcast()]


@app.route('/indoors_weather/')
def get_indoors_weather():
    (temperature,pressure)=bmc280.readBmp180()
    return {"temp": temperature, "pressure": pressure}


if __name__ == "__main__":
    app.run(debug=True)
