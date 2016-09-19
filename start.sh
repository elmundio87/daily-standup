#!/usr/bin/env bash
./stop.sh
python -m SimpleHTTPServer &
python standup.py
