from celery_app import celery_app


def add_background_job(func, *args):
    run_background_job.delay(func, *args)


@celery_app.task
def run_background_job(func, *args):
    from src.background_jobs.job_map import background_jobs_map
    background_jobs_map[func](*args)
