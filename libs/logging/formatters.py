import logging


class CallTraceFormatter(logging.Formatter):
    """
    Форматтер для формирования единой строки используемой в форматировании
    Помогает выравнивать запись вида [%(module).%(funcName):%(lineno)d] до 64 символов вроде этого:
        [logger.method_with_looong_looong_ooloong_name:91                ]
        or
        [main.<module>:5                                                 ]
    """

    def format(self, record):
        record.custom_call_trace = f"{record.module}.{record.funcName}:{record.lineno}"

        return super().format(record)


# https://www.distributedpython.com/2018/11/06/celery-task-logger-format/
class TaskFormatter(CallTraceFormatter):
    """
    Форматтер для подстановки идентификатора таска в форматированный вывод лога
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            from celery._state import get_current_task
            self.get_current_task = get_current_task
        except ImportError:
            self.get_current_task = lambda: None

    def format(self, record):
        task = self.get_current_task()
        if task and task.request:
            record.__dict__.update(task_id=task.request.id,
                                   task_name=task.name)
        else:
            record.__dict__.setdefault('task_name', '')
            record.__dict__.setdefault('task_id', '')
        return super().format(record)