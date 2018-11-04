#!/usr/bin/env sh

export FLASK_APP=server
FLASK_ENV=development flask run --host=0.0.0.0 --port=8000
