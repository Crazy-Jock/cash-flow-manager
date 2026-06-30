#!/bin/sh

echo "Waiting for postgres..."

until pg_isready -h db -p "${POSTGRES_PORT}" -U "${USER_DB}"; do
  sleep 1
done

echo "Postgres started"

python manage.py migrate
python manage.py collectstatic --noinput

exec python manage.py runserver 0.0.0.0:8000