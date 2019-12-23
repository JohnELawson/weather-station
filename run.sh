#!/bin/bash

# cd ~/Documents/weather-stations
source env/bin/activate
# pip install -r requirements.txt
source ./exports.sh 

DISPLAY=:0 chromium-browser -start-fullscreen http://127.0.0.1:5000/ &

python3 main.py
