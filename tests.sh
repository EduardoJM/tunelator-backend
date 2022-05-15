#!/bin/sh

while ! nc -z localhost 8000 ; do
    echo "Waiting for the api server"
    sleep 0.1
done

docker exec api python manage.py test
