from celery import Celery
import os

celery_app = Celery('celery_jobs_manager', broker=os.getenv('CELERY_BROKER') or 'redis://localhost:6379/0', include=['src.background_jobs.celery_background_tasks_wrapper'])