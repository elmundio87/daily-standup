# daily-standup [![Build Status](https://travis-ci.org/elmundio87/daily-standup.svg?branch=master)](https://travis-ci.org/elmundio87/daily-standup)
A dashboard that can be shown at the beginning of each day during a standup.

# I just want to add a new hostname to the Live SSL report!

Fork this repo, update `config/expiring_certs_config.py` and create a Pull Request.

# Getting started

Create a virtualenv and install all dependencies `pip install -r requirements.txt`

Make a copy of `config/config.py.sample` called `config/config.py` and edit as required.

The password hash can be generated using the command `echo -n your_password | sha256sum`

If you plan on running this in AWS, set up a profile using the AWS CLI called "daily-standup"

# Running the dashboard locally

Run: `./run-local.sh`

This will start the API server. You will then need to open static/index.html,
or host the `static` folder in a webserver.

Note that the webcam mirroring won't work if you are using the file:// protocol.
I recommend using `python -m SimpleHTTPServer` to stand up a quick webserver.

# Deploying to AWS

1. Create an S3 bucket to host the static html/css/js assets
2. Update the target bucket in `deploy.sh` to match the bucket you created
3. Change the 's3_bucket' configuration in `zappa_settings.json` to a unique name
4. Run `deploy-dev.sh` to install the API gateway and the lambda function or `deploy-live.sh` to deploy the API Gateway, Lambda and static assets.
5. In the AWS Console, create a cloudfront configuration that points at the static assets bucket, with a SSL certificate attached.

If the URL is not served over https, the webcam mirroring will not function
