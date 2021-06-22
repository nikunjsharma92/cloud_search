#!/usr/bin bash

celery -A celery_app.celery_app worker --concurrency=7 --loglevel=INFO