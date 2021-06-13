from celery import Celery
import os

celery_app = Celery('celery_jobs_manager', backend='redis://localhost:6379/1', broker=os.getenv('CELERY_BROKER') or 'redis://localhost:6379/0')