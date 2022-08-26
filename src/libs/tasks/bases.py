from celery import Task
from loguru import logger


class LoggedTask(Task):
    def __call__(self, *args, **kwargs):
        with logger.contextualize(task_id=self.request.id):
            logger.info(f"Start <{self.name}> task.")
            result = super().__call__(*args, **kwargs)
            logger.info(f"End of task <{self.name}>.")

            return result
