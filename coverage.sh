#!/bin/sh

while ! nc -z localhost 8000 ; do
    echo "Waiting for the api server"
    sleep 0.1
done

docker exec api coverage run --source='.' manage.py test
#docker exec api coverage json --omit='*migrations*,*/**/admin.py,*tests*,core/asgi.py,core/wsgi.py,manage.py'
#docker exec api coverage html --omit='*migrations*,*/**/admin.py,*tests*,core/asgi.py,core/wsgi.py,manage.py'
#docker exec api coverage report --omit='*migrations*,*/**/admin.py,*tests*,core/asgi.py,core/wsgi.py,manage.py'
