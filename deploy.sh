#!/bin/bash

zappa deploy
zappa update

API_URL=$(zappa status | grep "API Gateway URL:" | sed 's|API Gateway URL:||' | xargs)

mkdir -p static/properties
echo "var API_URL = \"${API_URL}\"" > static/properties/urls.js

aws s3 cp --recursive --include "*" static s3://static-dog-dailystandup-dev
