import pprint

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from libs.logging.logger2 import Logger

pp = pprint.PrettyPrinter(indent=4, depth=10, width=128)


class LoggedSerializerWrapper(Logger):
    logged_methods = []

    def __getattribute__(self, name):
        attr = super().__getattribute__(name)

        if name != "logged_methods" and name in self.logged_methods:
            self.logger.debug(f"Call `{name}`")

            return self.__logged_wrapper(attr)
        else:
            return attr

    def __logged_wrapper(self, method):
        def wrapper(*args, **kwargs):
            self.logger.debug(f"\n  args:\n{pp.pformat(args)}\n  kwargs:\n{pp.pformat(kwargs)}\n")
            return method(*args, **kwargs)

        return wrapper


class DatetimeListField(serializers.ListField):
    child = serializers.DateTimeField()

