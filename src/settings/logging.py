import sys

from loguru import logger

from libs.utils.logging import not_any_of
from .environment import DEBUG

__all__ = ["LOG_LEVEL"]

LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

LOGGING = {
    "version": 1,
    'disable_existing_loggers': True,
    "handlers": {
        "loguru": {
            "level": LOG_LEVEL,
            "class": "libs.logging.handlers.InterceptHandler"
        }
    },
    "loggers": {
        "django": {
            "handlers": ["loguru"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["loguru"],
            "level": "INFO",
            "propagate": False,
        },
    }
}


# LOGGING_CONFIG = None


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
