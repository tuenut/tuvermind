import copy
import logging
import logging.config
import logging.handlers
import os

from settings import LOG_DIR, LOGGING, LOG_LEVEL


class Logger:
    log_level = LOG_LEVEL
    LOGGING = copy.deepcopy(LOGGING)
    __log_dir = LOG_DIR

    __default_logger = {
        'level': log_level,
        'handlers': [],
        'propagate': False,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__check_dirs()
        self.__configure()

        logging.config.dictConfig(self.LOGGING)

        self.logger = logging.getLogger(self.__logger_name)

    def __check_dirs(self):
        try:
            os.mkdir(self.__log_dir)
        except OSError as e:
            if e.errno == 17:
                pass
            else:
                raise

    def __configure(self):
        for handler in self.LOGGING["handlers"]:
            if "filename" in handler:
                handler["filename"] = self.__log_file

        logger_config = copy.deepcopy(self.__default_logger)
        logger_config["handlers"] = list(self.LOGGING["handlers"].keys())

        self.LOGGING['loggers'].update({self.__logger_name: logger_config})

    @property
    def __log_file(self):
        file_name = os.path.join(self.__module_path, self.__class_name + '.log')

        return os.path.join(LOG_DIR, file_name)

    @property
    def __module_path(self):
        return '/'.join(self.__module__.split('.'))

    @property
    def __class_name(self):
        return self.__class__.__name__

    @property
    def __logger_name(self):
        return f"{self.__module__}.{self.__class__.__name__}"
