#!/bin/sh

echo "Running entrypoint..."

if [ "$DATABASE_TYPE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $PSG_HOST $PSG_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "Finished entrypoint..."

exec "$@"