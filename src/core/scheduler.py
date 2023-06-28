from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pymongo import MongoClient
from pytz import utc

from src.core.singleton import Singleton
from src.settings import settings


class ServiceScheduler(AsyncIOScheduler, Singleton):
    def __init__(self, *args, **kwargs):
        super(ServiceScheduler, self).__init__(*args, **kwargs)
        job_store = MongoDBJobStore(
            database=settings.MONGO_SETTINGS.MONGO_SCHEDULE_TASKS_DB_NAME,
            collection=settings.MONGO_SETTINGS.MONGO_SCHEDULE_TASKS_COLLECTION_NAME,
            client=MongoClient(settings.SCHEDULER_URL)
        )
        self.add_jobstore(job_store)


service_scheduler = ServiceScheduler(
    timezone=utc
)
