#!/usr/bin bash

set -e
echo "Running readiness probe"
python check_readiness.py
echo "Starting db migrations"
flask db upgrade
echo "Starting elastic migrations"
python elasticsearch_migrations.py
echo "Starting Api Server"
gunicorn --bind 0.0.0.0:8080 app:app