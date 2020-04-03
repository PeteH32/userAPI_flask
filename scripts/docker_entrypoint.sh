#!/bin/sh

# For WSGI layer, using gunicorn: https://docs.gunicorn.org
gunicorn --workers 1 --bind 0.0.0.0:5000 app:app
