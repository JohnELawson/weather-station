#!/bin/bash

# cd ~/Documents/weather-stations
source env/bin/activate
# pip install -r requirements.txt
source ./exports.sh 

DISPLAY=:0 chromium-browser --kiosk  --disable-info-bars -start-fullscreen --app=http://127.0.0.1:5000/&

python3 main.py
