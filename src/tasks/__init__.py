from loguru import logger

from celery import shared_task

from libs.tasks.bases import LoggedTask


@shared_task(base=LoggedTask)
def test_loguru_task():
    logger.info(f"Start loguru testing task.")
    logger.debug(f"Send some DEBUG message.")

    try:
        1 / 0
    except:
        logger.exception(f"Test EXCEPTION message.")

    logger.error(f"Test ERROR message.")
    logger.critical(f"Test CRITICAL message.")
    logger.info(f"Testing loguru logging task complete.")
