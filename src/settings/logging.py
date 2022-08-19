import sys

from loguru import logger

from libs.utils.logging import not_any_of
from .environment import DEBUG


__all__ = ["LOGGING_CONFIG", "LOG_LEVEL"]

LOGGING_CONFIG = None
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

api_logs_filter = lambda record: "request_id" in record["extra"]
celery_logs_filter = lambda record: "task_id" in record["extra"]
fallback_logs_filter = not_any_of(api_logs_filter, celery_logs_filter)

api_logs_format = "{time} | {level} | {extra[request_id]} | {message}"
celery_logs_format = "{time} | {level} | {extra[task_id]} | {message}"
fallback_logs_format = "{time} | {level} | {message}"

api_handler_config = dict(
    sink=sys.stderr,
    level=LOG_LEVEL,
    format=api_logs_format,
    backtrace=True,
    filter=api_logs_filter
)
celery_handler_config = dict(
    sink=sys.stderr,
    level=LOG_LEVEL,
    format=celery_logs_format,
    backtrace=True,
    filter=celery_logs_filter
)
fallback_handler_config = dict(
    sink=sys.stderr,
    level=LOG_LEVEL,
    format=fallback_logs_format,
    backtrace=True,
    filter=fallback_logs_filter
)

logger.configure(
    handlers=[
        api_handler_config,
        celery_handler_config,
        fallback_handler_config
    ]
)
