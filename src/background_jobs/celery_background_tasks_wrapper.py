from celery_app import celery_app

def add_background_job(key, *args):
    run_background_job.delay(key, *args)


@celery_app.task(bind=True)
def run_background_job(self, func, *args):
    from app import app
    with app.app_context():
        from src.background_jobs.job_map import background_jobs_map
        background_jobs_map[func](*args)