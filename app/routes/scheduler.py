from typing import Dict

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from fastapi_utils.inferring_router import InferringRouter

# from app.depends.db_depend import get_db as campaign_db
# from app.utils import catch_not_implemented_exception
from app.custom_classes.job_manager import PrintJobManager, CharacterExtractorManager, PreOcrCharacterLoad
from db.database import SessionLocal

app: FastAPI = FastAPI(title='fast-api')

scheduler: BackgroundScheduler = None
router = InferringRouter()


@router.on_event('startup')
def init_scheduler():
    db = SessionLocal()
    job_stores: Dict = {
        'default': SQLAlchemyJobStore(url='sqlite:///app/jobs.sqlite')
    }
    executors: Dict = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }
    job_defaults: Dict = {
        'coalesce': False,
        # 'max_instances': 3
    }
    global scheduler
    from apschedulerui.web import SchedulerUI
    global scheduler
    scheduler = BackgroundScheduler(jobstores=job_stores,
                                    executors=executors,
                                    job_defaults=job_defaults)
    ui = SchedulerUI(scheduler, capabilities={'pause_job': True, 'remove_job': True, 'pause_scheduler': True,
                                              'stop_scheduler': True, 'run_job': True})
    ui.start()
    scheduler.configure(jobstores=job_stores,
                        # executors=executors
                        )
    from db.models import ScheduleJobNames

    from app.custom_classes.schedule import Scheduler as ThirdPartyScheduler
    ThirdPartyScheduler().start()
    job_list = scheduler.get_jobs()
    print(job_list)

    # job_initiator(db, job_list, scheduler, ScheduleJobNames.PrintJobManager, '*/1 * * * *',
    #               PrintJobManager.execute)
    # job_initiator(db, job_list, scheduler, ScheduleJobNames.CharacterExtractorManager, '*/1 * * * *',
    #               CharacterExtractorManager.execute)
    job_initiator(db, job_list, scheduler, ScheduleJobNames.PreOcrCharacterLoad, '*/1 * * * *',
                  PreOcrCharacterLoad.execute)


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
