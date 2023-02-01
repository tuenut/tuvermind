import sys

from loguru import logger

from libs.logging.loguru_configuration import (
    has_extra_key,
    HandlerConfig,
    LoguruHandlersConfig,
    not_any_of,
)
from .environment import DEBUG


__all__ = ["LOG_LEVEL"]

LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "loguru": {
            "level": LOG_LEVEL,
            "class": "libs.logging.handlers.InterceptHandler",
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
    },
}

LOG_REQUEST_ID_HEADER = "HTTP_X_REQUEST_ID"
GENERATE_REQUEST_ID_IF_NOT_IN_HEADER = True
REQUEST_ID_RESPONSE_HEADER = "REQUEST_ID"


class Configuration(LoguruHandlersConfig):
    _default_level = LOG_LEVEL
    _default_sink = sys.stderr
    _default_backtrace = False

    api_default = HandlerConfig(
        format="{time} | {level} | {extra[request_id]} | {message}",
        filter=has_extra_key("request_id"),
    )
    celery_default = HandlerConfig(
        format="{time} | {level} | {extra[task_id]} | {message}",
        filter=has_extra_key("task_id"),
    )
    fallback_default = HandlerConfig(
        format="{time} | {level} | {message}",
        filter=not_any_of(
            has_extra_key("request_id"), has_extra_key("task_id")
        ),
    )


logger.configure(handlers=Configuration().get_handlers_config())
