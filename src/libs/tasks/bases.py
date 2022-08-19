from celery import Task
from loguru import logger


class LoggedTask(Task):
    def __call__(self, *args, **kwargs):
        with logger.contextualize(task_id=self.request.id):
            return super().__call__(*args, **kwargs)
