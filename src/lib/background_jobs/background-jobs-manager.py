class BackgroundJobsManager:
    def __init__(self, client):
        self.__client = client

    def add_job(self, job_name, job_args):
        self.__client.add_job(job_name, job_args)
