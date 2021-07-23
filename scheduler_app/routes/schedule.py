from typing import Dict

from apscheduler.events import (EVENT_JOB_SUBMITTED,
                                EVENT_JOB_REMOVED,
                                EVENT_JOB_ADDED,
                                EVENT_JOB_ERROR,
                                EVENT_JOB_MISSED,
                                EVENT_JOB_MODIFIED,
                                EVENT_JOB_MAX_INSTANCES,
                                EVENT_JOB_EXECUTED)
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from fastapi_utils.inferring_router import InferringRouter

# from app.depends.db_depend import get_db as campaign_db
# from app.utils import catch_not_implemented_exception
from db.database import SessionLocal
from scheduler_app.services.schedule import SchedulerService
from scheduler_app.third_party_clients.job_manager import PrintJobManager, ContactCampaignEmailGenerationManager, TaskDueJobNotificationJobManager
from scheduler_app.third_party_clients.scheduler_event import SchedulerEvent

app: FastAPI = FastAPI(title='fast-api')

scheduler: BackgroundScheduler = None
router = InferringRouter()


@router.on_event('startup')
def init_scheduler():
    db = SessionLocal()
    job_stores: Dict = {
        'default': SQLAlchemyJobStore(url='sqlite:///scheduler_app/jobs.sqlite')
    }
    # executors: Dict = {
    #     'default': ThreadPoolExecutor(20),
    #     'processpool': ProcessPoolExecutor(5)
    # }
    job_defaults: Dict = {
        'coalesce': False,
        # 'max_instances': 3
    }
    global scheduler
    from apschedulerui.web import SchedulerUI
    global scheduler
    scheduler = BackgroundScheduler(jobstores=job_stores,
                                    # executors=executors,
                                    job_defaults=job_defaults)
    ui = SchedulerUI(scheduler, capabilities={'pause_job': True, 'remove_job': True, 'pause_scheduler': True,
                                              'stop_scheduler': True, 'run_job': True})
    ui.start()
    scheduler.configure(jobstores=job_stores,
                        # executors=executors
                        )
    scheduler.add_listener(SchedulerEvent().on_job_submitted, EVENT_JOB_SUBMITTED)
    scheduler.add_listener(SchedulerEvent().on_job_removed, EVENT_JOB_REMOVED)
    scheduler.add_listener(SchedulerEvent().on_job_added, EVENT_JOB_ADDED)
    scheduler.add_listener(SchedulerEvent().on_job_missed, EVENT_JOB_MISSED)
    scheduler.add_listener(SchedulerEvent().on_job_error, EVENT_JOB_ERROR)
    scheduler.add_listener(SchedulerEvent().on_job_max_instances, EVENT_JOB_MAX_INSTANCES)
    scheduler.add_listener(SchedulerEvent().on_job_modified, EVENT_JOB_MODIFIED)
    scheduler.add_listener(SchedulerEvent().on_job_executed, EVENT_JOB_EXECUTED)
    from db.models import ScheduleJobNames

    from scheduler_app.custom_classes.schedule import Scheduler as ThirdPartyScheduler
    ThirdPartyScheduler().start()
    job_list = scheduler.get_jobs()
    print(job_list)

    job_initiator(db, job_list, scheduler, ScheduleJobNames.CharacterSegmentationManager, '0 */6 * * *',
                  TaskDueJobNotificationJobManager.execute)
    # job_initiator(db, job_list, scheduler, ScheduleJobNames.ContactCampaignEmailGenerationManager, '1-59 * * * *',
    #               ContactCampaignEmailGenerationManager.execute)


def job_initiator(db, job_list, scheduler, schedule_job_names, cron_tab, job_func):
    add_job_flag = True

    for jb in job_list:
        print(jb.name, schedule_job_names)
        if jb.name == schedule_job_names:
            # print(jb.name, schedule_job_names)
            add_job_flag = False
            break
    if add_job_flag:
        job = scheduler.add_job(func=job_func, trigger=CronTrigger.from_crontab(cron_tab),
                                name=schedule_job_names)
        # crud_object = SchedulerService()
        # job_object = crud_object.create_schedule_job(db=db, job_id=job.id, name=schedule_job_names)
        # job_log_object = crud_object.create_schedule_job_log(db=db, job_id=job_object.id, run_status="Added")

# @cbv(router)
# class Scheduler(object):
#     db: Session = Depends(campaign_db)

#     # @router.post("/add-job/{function_name}/{trigger}", status_code=status.HTTP_201_CREATED)
#     # @catch_not_implemented_exception
#     # def add_job(self, function_name: str = Path(...), function_kwargs: Dict = Body(...),
#     #             trigger: TriggerRegister = Path(...), trigger_kwargs: Dict = Body(...),
#     #             job_options: JobOptions = Body(...), cron_enable: Optional[bool] = Query(False)):
#     #     scheduler_service_object = SchedulerService().add_job(db=self.db, func_name=function_name,
#     #                                                           function_kwargs=function_kwargs, trigger=trigger,
#     #                                                           trigger_kwargs=trigger_kwargs, job_options=job_options,
#     #                                                           cron_enable=cron_enable)
#     #
#     #     if scheduler_service_object:
#     #         return {
#     #             "success": True,
#     #             "data": scheduler_service_object
#     #         }
#     #     else:
#     #         return {
#     #             "success": False
#     #         }
#     #
#     # #
#     @router.post("/stop-job/{job_id}", status_code=status.HTTP_201_CREATED)
#     @catch_not_implemented_exception
#     def remove_job(self, job_id: str = Path(...)):
#         from scheduler_app.third_party_clients.schedule import Scheduler as ThirdPartyScheduler
#         tp_scheduler = ThirdPartyScheduler()
#         job = tp_scheduler.remove_job(job_id=job_id)
#         return job
#         # tp_scheduler.start()

#     @router.get("/get-jobs")
#     @catch_not_implemented_exception
#     def get_jobs(self):
#         scheduler_service_object = SchedulerService().get_all_jobs(db=self.db)
#         return scheduler_service_object
#         # return job_list
#     #
#     # @router.post("/add-job-hold/{function_name}", status_code=status.HTTP_201_CREATED)
#     # @catch_not_implemented_exception
#     # def add_interval_job_hold(self, function_name: str = Path(...)):
#     #     from scheduler_app.third_party_clients.schedule import Scheduler as ThirdPartyScheduler
#     #     tp_scheduler = ThirdPartyScheduler()
#     #     job = tp_scheduler.add_interval_job(func=getattr(jobs.Jobs(), function_name), seconds=3)
#     #     job = tp_scheduler.pause_job(job_id=job.id)
#     #     return job
#     #     # tp_scheduler.start()
