#!/bin/bash

source ./env/bin/activate
./exports.sh
python3 main.py

/usr/bin/firefox 127.0.0.1:5000
