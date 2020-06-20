import copy
import logging
import logging.config
import logging.handlers
import os

from settings import LOG_DIR, LOGGING, LOG_LEVEL


class Logger(type):
    """"
    :param log_level: default log level set in settings.py
    :param default_logger: шаблон логера
    :param handlers: list of handler names, which will be added to the logger.
    :param override_%handler_name%: dict where may be override some parameters
     of existed %handler_name% or setup new handler. If that new handler, need
     add its name to handlers list if you want add it to current logger.
     New handler will be exists for all child of class, where it described.
     Examples:
                override_basic_stream = {
                    'level': 100,
                    'formatter': 'basic_formatter',
                }
                override_new_stream = {
                    'level': LOG_LEVEL,
                    'class': 'logging.StreamHandler',
                    "stream": "ext://sys.stdout"
                }
     If handler has 'filename' and its None, then use default filename with
     module dirs structure, else if filename is str, then use it like a
     relative path, starts with $BASE_DIR/logs/
     Exapmle:
                override_custom_file = {
                    'filename': 'path/to/file.log'
                }
        then log file will saved in $BASE_DIR/logs/path/to/file.log

    All default configuration described in settings.py in LOGGING var
    """

    log_level = LOG_LEVEL
    handlers = ['basic_file', 'basic_stream']

    __default_logger = {
        'level': log_level,
        'handlers': [],
        'propagate': False,
    }

    def __init__(cls, name, bases, dct, *args, **kwargs):
        cls.get_logger_name = "%s.%s" % (cls.__module__, name)

        logging.addLevelName(41, 'SlackErrors')

        cls.LOGGING = copy.deepcopy(LOGGING)

        cls.__default_setup_logger()
        cls.__reconfigure_handlers()

        cls.__check_log_dirs()
        logging.config.dictConfig(cls.LOGGING)

        cls.logger = logging.getLogger(cls.get_logger_name)
        cls.logger.setLevel(cls.log_level)

        cls.logger.addFilter(CallTraceFilter())

        super().__init__(name, bases, dct,)

    def __default_setup_logger(self):
        # Get empty logger.
        logger = copy.deepcopy(self.__default_logger)

        # Get default handlers from LOGGING by names in self.handlers.
        handlers = {
            self.get_handler_name(key): self.LOGGING['handlers'][key]
            for key in self.LOGGING['handlers'] if key in self.handlers
        }
        logger['handlers'].extend([hndlr for hndlr in handlers])

        # Set filename if FileHandler or same.
        for handler in handlers:
            if 'filename' in handlers[handler]:
                handlers[handler]['filename'] = self.__get_file_name()

        self.LOGGING['loggers'].update({self.get_logger_name: logger})
        self.LOGGING['handlers'].update(handlers)

    def __reconfigure_handlers(self):
        for attr in dir(self):
            if attr.startswith('override_') and attr[len('override_'):] in self.handlers:
                handler_prfx = attr[len('override_'):]
                handler_name = self.get_handler_name(handler_prfx)
                handler_dict = getattr(self, attr)

                if 'filename' in handler_dict:
                    file_name = handler_dict['filename']
                    handler_dict['filename'] = self.__get_file_name(file_name)
                try:
                    self.LOGGING['handlers'][handler_name].update(handler_dict)
                except KeyError:
                    self.LOGGING['handlers'][handler_name] = handler_dict

    def __get_file_name(self, file_name=None):
        if file_name is None:
            module_path = '/'.join(self.get_logger_name.split('.')[:-1])
            class_name = self.get_logger_name.split('.')[-1]
            file_name = os.path.join(module_path, class_name+'.log')

        full_file_path = os.path.join(LOG_DIR, file_name)
        return full_file_path

    def __check_log_dirs(self):
        for handler_prfx in self.handlers:
            handler_name = self.get_handler_name(handler_prfx)
            if 'filename' in self.LOGGING['handlers'][handler_name]:
                root_path = self.LOGGING['handlers'][handler_name]['filename']
                root_path = os.path.dirname(root_path)
                if not os.path.exists(root_path):
                    os.makedirs(root_path, exist_ok=True)

    def get_handler_name(self, handler_prefix_name):
        return "%s.%s" % (handler_prefix_name, self.get_logger_name)


class CallTraceFilter(logging.Filter):
    """
    Aligning [%(module).%(funcName):%(lineno)d] to 64 symbols like that:
        [logger.method_with_looong_looong_ooloong_name:91                ]
        or
        [main.<module>:5                                                 ]

    """
    def filter(self, record):
        record.custom_call_trace = '{}.{}:{}'.format(
            record.module, record.funcName, record.lineno
        )
        return True


class TaskIdFilter(logging.Filter):
    """
    For adding %(task_id) attribute to log filter. Get it
    """
    def __init__(self, *args, **kwargs):
        try:
            self.task_id = kwargs.pop('task_id')
        except:
            self.task_id = 'No task id'

    def filter(self, record):
        record.task_id = self.task_id
        return True

