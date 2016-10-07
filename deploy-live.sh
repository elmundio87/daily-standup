#!/bin/bash

zappa deploy live
zappa update live

API_URL=$(zappa status live | grep "API Gateway URL:" | sed 's|API Gateway URL:||' | xargs)

mkdir -p static/properties
echo "var API_URL = \"${API_URL}\"" > static/properties/urls.js

aws s3 cp --recursive --include "*" static s3://static-dog-dailystandup-live --profile "daily-standup"
