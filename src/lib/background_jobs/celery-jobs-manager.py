from celery_app import celery_app


class CeleryJobsManager:
    def __init__(self, celery_app):
        self.app = celery_app

    def add_job(self, func, args):
        self.run_job.delay(func, args)

    @celery_app.task
    def run_job(self, func, args):
        func.delay(args)
