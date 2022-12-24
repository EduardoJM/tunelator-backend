#!/bin/sh

export FLASK_APP=app:create_app
gunicorn -b 0.0.0.0:5000 app.wsgi:app
