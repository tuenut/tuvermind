import sys
from typing import Union

from loguru import logger

from .environment import DEBUG

__all__ = ["LOGGING_CONFIG", "LOG_LEVEL"]

LOGGING_CONFIG = None
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"


def combine_with(modifier: Union[all, any], inverse=False):
    def combine_filters(*filters):
        def combined_filter(record):
            result = modifier([fn(record) for fn in filters])
            return not result if inverse else result

        return combined_filter

    return combine_filters


not_any_of = combine_with(any, inverse=True)

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
    backtrace=False,
    serialize=True,
    filter=api_logs_filter
)
celery_handler_config = dict(
    sink=sys.stderr,
    level=LOG_LEVEL,
    format=celery_logs_format,
    backtrace=False,
    serialize=True,
    filter=celery_logs_filter
)
fallback_handler_config = dict(
    sink=sys.stderr,
    level=LOG_LEVEL,
    format=fallback_logs_format,
    backtrace=False,
    serialize=True,
    filter=fallback_logs_filter
)

logger.configure(
    handlers=[
        api_handler_config,
        celery_handler_config,
        fallback_handler_config
    ],
    extra={"special_fluentd_tag": True}
)
