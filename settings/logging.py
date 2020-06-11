import logging

__all__ = ["LOG_LEVEL", "LOGGING"]

LOG_LEVEL = logging.DEBUG
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)-8s >> [%(custom_call_trace)-36s] [%(process)d] [%(thread)d] %(message)s'
        },
        'task_formatter': {
            'format': '%(asctime)s %(levelname)-8s >> [%(custom_call_trace)-36s] [Task: %(task_id)s] %(message)s'
        },
        'basic_formatter': {
            'format': '%(asctime)s %(levelname)-8s >> [%(custom_call_trace)-36s] %(message)s'
        },
        'slack_formatter': {
            'format': '%(message)s'
        },
    },
    'filters': {},
    'loggers': {},
    'handlers': {
        'basic_stream': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'basic_formatter',
            "stream": "ext://sys.stdout"
        },
        'basic_file': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'basic_formatter',
            'when': 'W6',
            'interval': 1,
            'backupCount': 10,
            'filename': 'default.log'
        },
    }
}