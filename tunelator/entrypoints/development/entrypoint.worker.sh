#!/bin/sh

while ! nc -z redis 6379 ; do
    echo "Waiting for the Redis Server"
    sleep 3
done
while ! nc -z db 5432 ; do
    echo "Waiting for the MySQL Server"
    sleep 3
done

celery -A core worker --beat --loglevel=info
