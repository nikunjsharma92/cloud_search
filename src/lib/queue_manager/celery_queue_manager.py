from celery import Celery
import os

queue_manager = Celery('queue_manager', broker=os.getenv('CELERY_BROKER'))
