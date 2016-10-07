#!/bin/bash

pip install s3cmd
pip install awscli

aws configure set aws_access_key_id $aws_access_key_id --profile "daily-standup"
aws configure set aws_secret_access_key $aws_secret_access_key --profile "daily-standup"
aws configure set region eu-west-1 --profile "daily-standup"
aws configure set output json --profile "daily-standup"

if [ "$TRAVIS_BRANCH" = "master" ]; then
  ./deploy-live.sh
else
  echo "Don't deploy non-master builds to live"
fi
