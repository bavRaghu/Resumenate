#!/bin/bash

apt-get update

apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    shared-mime-info

gunicorn --timeout 300 main:app