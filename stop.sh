#!/usr/bin/env bash
echo -e "Killing any processes that are using port 8000"
kill -9 $(lsof -t -i:8000)
