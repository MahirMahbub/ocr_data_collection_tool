# import datetime
#
# from apscheduler.triggers.base import BaseTrigger
#
#
# class IntervalTrigger(BaseTrigger):
#     def __init__(self, seconds=0, minutes=0, hours=0, days=0, milliseconds=0, weeks=0, microseconds=0):
#         self.seconds = seconds
#         self.minutes = minutes
#         self.hours = hours
#         self.days = days
#         self.milliseconds = milliseconds
#         self.weeks = weeks
#         self.microseconds = microseconds
#
#     def get_next_fire_time(self, previous_fire_time, now):
#         next_fire_time = previous_fire_time + datetime.timedelta(days=self.days, seconds=self.seconds, hours=self.hours,
#                                                                  microseconds=self.microseconds,
#                                                                  milliseconds=self.milliseconds, minutes=self.minutes,
#                                                                  weeks=self.weeks)
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger


class BuildInJobTrigger(object):
    def __new__(cls, trigger, cron_enable, **kwargs):
        register = {}
        register["Interval"] = IntervalTrigger
        print(list(kwargs.values()))
        register["Date"] = DateTrigger
        if cron_enable:
            register["Cron"] = CronTrigger.from_crontab(list(kwargs.values())[0])
            return register["Cron"]
        else:
            register["Cron"] = CronTrigger
        return register[trigger](**kwargs)
