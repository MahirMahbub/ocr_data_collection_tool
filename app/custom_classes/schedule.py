import logging

from db.schemas import JobOptions
from app.custom_classes.job_trigger import BuildInJobTrigger

# logging.basicConfig(filename='scheduler_app/schedule.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)


class Scheduler(object):

    @staticmethod
    def add_job(func, kwargs, trigger, trigger_kwargs, job_options: JobOptions, cron_enable):
        from app.routes.scheduler import scheduler
        job_ = scheduler.add_job(func=func, kwargs=kwargs,
                                 trigger=BuildInJobTrigger(trigger=trigger, cron_enable=cron_enable, **trigger_kwargs),
                                 name=job_options.name, misfire_grace_time=job_options.misfire_grace_time,
                                 coalesce=job_options.coalesce,
                                 max_instances=job_options.max_instances,
                                 max_runs = job_options.max_runs)
        return job_

    @staticmethod
    def remove_job(job_id):
        from app.routes.scheduler import scheduler
        scheduler.remove_job(job_id)
        logging.info("Job-ID: %s, Operation: Removed".format(str(job_id)))

    @staticmethod
    def pause_job(job_id):
        from app.routes.scheduler import scheduler
        scheduler.pause_job(job_id)
        logging.info("Job-ID: %s, Operation: Paused".format(str(job_id)))

    @staticmethod
    def resume_job(job_id):
        from app.routes.scheduler import scheduler
        logging.info("Job-ID: %s, Operation: Paused".format(str(job_id)))
        scheduler.resume_job(job_id)

    @staticmethod
    def get_jobs():
        from app.routes.scheduler import scheduler
        res = scheduler.get_jobs()
        return res

    @staticmethod
    def print_jobs():
        from app.routes.scheduler import scheduler
        scheduler.print_jobs()

    @staticmethod
    def start():
        from app.routes.scheduler import scheduler
        scheduler.start()
        logging.info("Scheduler Started")

    @staticmethod
    def shutdown():
        from app.routes.scheduler import scheduler
        scheduler.shutdown()
        logging.info("Scheduler Shutdown")

    def get_seconds_from_interval_time(self, interval_time):
        return interval_time.days * (
                3600 * 24) + interval_time.hours * 3600 + interval_time.minutes * 60 + interval_time.seconds
