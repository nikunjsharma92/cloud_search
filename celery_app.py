from celery import Celery
import os
import elasticsearch_connection

config = {}
celery_app = Celery('celery_jobs_manager', broker=os.getenv('CELERY_BROKER'), include=['src.background_jobs.celery_background_tasks_wrapper', 'app'], config_source=config)