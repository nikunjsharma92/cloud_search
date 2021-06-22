#!/usr/bin/env bash

flask db upgrade
python elasticsearch_migrations.py
gunicorn --bind 0.0.0.0:8080 app:app