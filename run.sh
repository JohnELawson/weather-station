#!/bin/bash

cd ~/Documents/weather-station
source env/bin/activate
# pip install -r requirements.txt
cat exports.txt | while read line; do export $line; done

DISPLAY=:0 chromium-browser -start-maximized http://127.0.0.1:5000/ &

python3 main.py
