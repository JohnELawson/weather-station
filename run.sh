#!/bin/bash

# pip install virtualenv
# source ./env/bin/activate
# pip install -r requirements.txt
. ./exports.sh

DISPLAY=:0 chromium-browser -start-maximized http://127.0.0.1:5000/ &

python3 main.py
