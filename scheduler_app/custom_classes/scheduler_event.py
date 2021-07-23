import datetime
import logging

from scheduler_app.enums import JobStatus
from db.database import SessionLocal
from db.schemas import ScheduledJobLogUpdate
from scheduler_app.cruds.jobs import Jobs as crudJob


class SchedulerEvent(object):
    def __init__(self):
        self.db = SessionLocal()

    def on_database_update(self, event, state, on_submission=False, on_finished=False):
        if on_submission:
            update_schema = ScheduledJobLogUpdate(run_status=state, start_datetime_utc=str(datetime.datetime.utcnow()))
        elif on_finished:
            update_schema = ScheduledJobLogUpdate(run_status=state, end_datetime_utc=str(datetime.datetime.utcnow()))
        else:
            update_schema = ScheduledJobLogUpdate(run_status=state)
        response = crudJob(db=self.db).update_job_log(job_id=event.job_id, job_details=update_schema)
        self.db.commit()
        if not response:
            logging.error("Job-ID: %s, Operation: Internal Database Update Failed".format(str(event.job_id)))

    def on_job_submitted(self, event):
        self.on_database_update(event, state=JobStatus.SUBMITTED, on_submission=True)
        logging.info("Job-ID: %s, Operation: Submitted".format(str(event.job_id)))

    def on_job_removed(self, event):
        self.on_database_update(event, state=JobStatus.STOPPED)
        logging.info("Job-ID: %s, Operation: Removed".format(str(event.job_id)))

    def on_job_paused(self, event):
        self.on_database_update(event, state=JobStatus.PAUSED)
        logging.info("Job-ID: %s, Operation: Paused".format(str(event.job_id)))

    def on_job_added(self, event):
        self.on_database_update(event, state=JobStatus.ADDED)
        logging.info("Job-ID: %s, Operation: Added".format(str(event.job_id)))

    def on_job_modified(self, event):
        self.on_database_update(event, state=JobStatus.MODIFIED)
        logging.info("Job-ID: %s, Operation: Modified".format(str(event.job_id)))

    def on_job_error(self, event):
        self.on_database_update(event, state=JobStatus.ERROR)
        logging.info("Job-ID: %s, Operation: Error".format(str(event.job_id)))

    def on_job_missed(self, event):
        self.on_database_update(event, state=JobStatus.MISSED)
        logging.info("Job-ID: %s, Operation: Missed".format(str(event.job_id)))

    def on_job_max_instances(self, event):
        self.on_database_update(event, state=JobStatus.MAX_INSTANCED)
        logging.info("Job-ID: %s, Operation: Max Instances Reached, Not Accepted".format(str(event.job_id)))

    def on_job_executed(self, event):
        self.on_database_update(event, state=JobStatus.EXECUTED, on_finished=True)
        logging.info("Job-ID: %s, Operation: Executed".format(str(event.job_id)))
