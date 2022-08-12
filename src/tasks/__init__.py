from celery import shared_task, Task
from loguru import logger


@shared_task(bind=True)
def test_loguru_task(self: Task):
    with logger.contextualize(task_id=self.request.id):
        logger.info(f"Start loguru testing task.")
        logger.debug(f"Send some DEBUG message.")

        try:
            1 / 0
        except:
            logger.exception(f"Test EXCEPTION message.")

        logger.error(f"Test ERROR message.")
        logger.critical(f"Test CRITICAL message.")
        logger.info(f"Testing loguru logging task complete.")
