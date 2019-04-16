#!/usr/bin/env bash

docker build -t ossi . && docker run -p 5000:5000 ossi