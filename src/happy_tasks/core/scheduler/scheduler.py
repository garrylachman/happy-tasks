from __future__ import annotations
from datetime import datetime
from mypy_extensions import TypedDict
from typing import Any, Dict, Optional
from types import FunctionType

from apscheduler.triggers.cron import CronTrigger
from apscheduler.job import Job
from apscheduler.events import JobEvent
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ProcessPoolExecutor

from happy_tasks.helpers.singleton import Singleton

class SchedulerFlowDetails(TypedDict, total=False):
    enabled: bool
    crontab: Optional[str]

class Scheduler(Singleton):
    scheduler: BackgroundScheduler
    
    def __init__(self, maxWorkers: int = 20, maxExecuters:int = 5):
        jobstores = {
            'default': MemoryJobStore()
        }
        executors = {
            'default': {'type': 'threadpool', 'max_workers': maxWorkers}
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 3
        }
        self.scheduler = BackgroundScheduler()
        self.scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
        self.scheduler.add_listener(self.onEvent)
        
    def onEvent(self, event: JobEvent):
        print(event)
        
    def addJob(self, crontabStr: str, func: FunctionType) -> Job:
        trigger: CronTrigger = None
        if crontabStr:
            trigger = CronTrigger.from_crontab(crontabStr)
        return self.scheduler.add_job(func, trigger)

    def parseCronTab(self, crontabStr: str) -> CronTrigger:
        return CronTrigger.from_crontab(crontabStr)