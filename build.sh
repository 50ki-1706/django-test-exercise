#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# Start the Django application with Gunicorn and Uvicorn worker
exec python -m gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000