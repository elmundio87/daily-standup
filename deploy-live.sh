#!/bin/bash

zappa deploy live
zappa update live

API_URL=$(zappa status live | grep "API Gateway URL:" | sed 's|API Gateway URL:||' | xargs)

mkdir -p static/properties
echo "var API_URL = \"${API_URL}\"" > static/properties/urls.js

aws_access_key_id="$(aws configure get aws_access_key_id --profile daily-standup)"
aws_secret_access_key="$(aws configure get aws_secret_access_key --profile daily-standup)"

s3cmd sync static/ s3://static-dog-dailystandup-live/ --delete-removed --no-mime-magic --guess-mime-type --access_key ${aws_access_key_id} --secret_key ${aws_secret_access_key}
