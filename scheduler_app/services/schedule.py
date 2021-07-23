# from scheduler_app.cruds.activity import Activity as crudActivity
# from scheduler_app.cruds.jobs import Jobs as crudJob
# 
# 
# class SchedulerService(object):
# 
#     def create_schedule_job(self, db, job_id, name, should_run=True):
#         crud_job_object = crudJob(db=db)
#         job_object = crud_job_object.create_job(job_id=job_id, name=name, should_run=should_run)
# 
#         db.commit()
#         return job_object
# 
#     def create_schedule_job_log(self, db, job_id, run_status):
#         crud_job_object = crudJob(db=db)
#         job_object = crud_job_object.create_job_log(job_id=job_id, run_status=run_status)
#         db.commit()
#         return job_object
# 
#     def get_all_jobs(self, db):
#         crud_job_object = crudJob(db=db)
#         response = crud_job_object.get_all_jobs()
#         return response
# 
#     def create_schedule_activity(self, db, name, should_run=True):
#         crud_activity_object = crudActivity(db=db)
#         activity_object = crud_activity_object.create_activity(name=name, should_run=should_run)
# 
#         db.commit()
#         return activity_object
# 
#     def create_schedule_activity_log(self, db, schedule_job_id, schedule_activity_id, run_status):
#         crud_activity_log_object = crudActivity(db=db)
#         job_object = crud_activity_log_object.create_activity_log(schedule_job_id=schedule_job_id,
#                                                                   schedule_activity_id=schedule_activity_id,
#                                                                   run_status=run_status)
#         db.commit()
#         return job_object
# 
#     def update_activity_log(self, db, activity_id, job_id, **kwargs):
#         from db.schemas import ScheduledActivityLogUpdate
#         update_dict = ScheduledActivityLogUpdate(**kwargs)
#         crud_activity_log_object = crudActivity(db=db)
#         response = crud_activity_log_object.update_activity_log(activity_id=activity_id,
#                                                                 job_id=job_id,
#                                                                 activity_details=update_dict)
#         db.commit()
#         return response
# 
#     def get_activity_id_by_name(self, db, name):
#         crud_activity_object = crudActivity(db=db)
#         return crud_activity_object.get_activity_id_by_name(name)
# 
#     def get_activity_job_id_by_activity_id(self, db, activity_id):
#         crud_activity_object = crudActivity(db=db)
#         return crud_activity_object.get_activity_job_id_by_activity_id(activity_id)
