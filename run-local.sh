#!/usr/bin/env bash

mkdir -p static/properties
echo "var API_URL = \"http://127.0.0.1:5000\"" > static/properties/urls.js

python server.py
