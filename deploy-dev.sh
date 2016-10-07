#!/bin/bash

zappa deploy dev
zappa update dev

API_URL=$(zappa status dev | grep "API Gateway URL:" | sed 's|API Gateway URL:||' | xargs)

mkdir -p static/properties
echo "var API_URL = \"${API_URL}\"" > static/properties/urls.js
