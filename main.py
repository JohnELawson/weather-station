import json
import logging
from flask import Flask, render_template
from flask_cors import CORS

from weather import get_weather, get_forcast, get_indoors

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
    return json.dumps([i.to_json() for i in get_forcast()])


@app.route('/indoors_weather/')
def get_indoors_weather():
    return get_indoors()


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == "__main__":
    app.run(debug=True)
