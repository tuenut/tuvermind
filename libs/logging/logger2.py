import pprint
import copy
import logging
import logging.config
import logging.handlers
import os

from settings import LOG_DIR, LOGGING, LOG_LEVEL


class Logger:
    LOGGING = copy.deepcopy(LOGGING)
    log_level = LOG_LEVEL

    __default_logger = {
        'level': log_level,
        'handlers': [],
        'propagate': False,
    }

    @property
    def logger_name(self):
        return f"{self.__module__}.{self.__class__.__name__}"

    def __init__(self, *args, **kwargs):
        self.__default_setup_logger()

        logging.config.dictConfig(self.LOGGING)

        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(self.log_level)
        pp = pprint.PrettyPrinter(indent=4, depth=10, width=128)

        self.logger.pformat = pp.pformat
        self._pretty_printer = pp

        super(Logger, self).__init__(*args, **kwargs)

    def __default_setup_logger(self):
        logger = copy.deepcopy(self.__default_logger)

        logger['handlers'] = list(self.LOGGING["handlers"].keys())

        # Set filename if FileHandler or same.
        for handler in self.LOGGING["handlers"].values():
            if 'filename' in handler:
                handler['filename'] = self.__get_filename()

        self.LOGGING['loggers'].update({
            self.logger_name: logger
        })

    def __get_filename(self):
        log_dir_path = os.path.join(LOG_DIR, self.__module__.replace(".", "/"))
        log_file_path = os.path.join(log_dir_path, f"{self.__class__.__name__}.log")

        os.makedirs(log_dir_path, exist_ok=True)

        return log_file_path
