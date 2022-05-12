import copy
import logging
import logging.config
import logging.handlers
import os

from settings import LOG_DIR, LOGGING, LOG_LEVEL


class Logger(type):
    LOGGING = copy.deepcopy(LOGGING)
    log_level = LOG_LEVEL

    __default_logger = {
        'level': log_level,
        'handlers': [],
        'propagate': False,
    }

    @property
    def class_logger_name(self):
        return f"{self.__module__}.{self.__class__.__name__}"

    @property
    def meta_logger_name(cls):
        return f"{cls.__module__}.{cls.__name__}"

    def __new__(mcs, name, bases, attrs):
        attrs.update({
            "LOGGING": Logger.LOGGING,
            "logger_name": mcs.class_logger_name,
            "logger": None
        })

        return super(Logger, mcs).__new__(mcs, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        cls.__default_setup_logger()

        logging.config.dictConfig(cls.LOGGING)

        cls.logger = logging.getLogger(cls.meta_logger_name)
        cls.logger.setLevel(cls.log_level)

        super(Logger, cls).__init__(name, bases, attrs)

    def __default_setup_logger(cls):
        logger = copy.deepcopy(cls.__default_logger)

        logger['handlers'] = list(cls.LOGGING["handlers"].keys())

        # Set filename if FileHandler or same.
        for handler in cls.LOGGING["handlers"].values():
            if 'filename' in handler:
                handler['filename'] = cls.__get_filename()

        cls.LOGGING['loggers'].update({
            cls.meta_logger_name: logger
        })

    def __get_filename(cls):
        log_dir_path = os.path.join(LOG_DIR, cls.__module__.replace(".", "/"))
        log_file_path = os.path.join(log_dir_path, f"{cls.__name__}.log")

        os.makedirs(log_dir_path, exist_ok=True)

        return log_file_path
