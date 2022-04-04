#!/bin/sh

while ! nc -z redis 6379 ; do
    echo "Waiting for the Redis Server"
    sleep 3
done
while ! nc -z db 5432 ; do
    echo "Waiting for the MySQL Server"
    sleep 3
done

gunicorn -b 0.0.0.0:8080 admin.wsgi:application
