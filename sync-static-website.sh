#!/bin/bash

aws s3 cp --recursive --include "*" static s3://static-dog-dailystandup-dev
