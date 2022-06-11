#!/bin/sh

while ! nc -z localhost 8000 ; do
    echo "Waiting for the api server"
    sleep 0.1
done

docker exec -ti api coverage run --source='.' manage.py test
docker exec -ti api coverage json --omit='*migrations*'
docker exec -ti api coverage html --omit='*migrations*'
