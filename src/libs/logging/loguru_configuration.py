from abc import ABC
from dataclasses import dataclass
from typing import Union, Optional, Any, Callable


def combine_with(modifier: Union[all, any], inverse=False):
    """Helper function to create complex  logger filters in functional style."""

    def combine_filters(*filters):
        def combined_filter(record):
            result = modifier([fn(record) for fn in filters])
            return not result if inverse else result

        return combined_filter

    return combine_filters


not_any_of = combine_with(any, inverse=True)


def has_extra_key(key_name: str):
    return lambda record: key_name in record["extra"]


@dataclass
class HandlerConfig:
    sink: Optional[Any] = None
    level: Optional[str | int] = None
    format: Optional[str | Callable] = None
    filter: Optional[Callable[[dict], bool] | str | dict] = None
    serialize: Optional[bool] = None
    backtrace: Optional[bool] = None
    diagnose: Optional[bool] = None
    colorize: Optional[bool] = None
    enqueue: Optional[bool] = None
    catch: Optional[bool] = None
    kwargs: Optional[dict[any]] = None


class LoguruHandlersConfig(ABC):
    """
    Класс нужен для генерации списка конфигов для хэндлеров loguru.

    Перебираем все атрибуты класса, которые не начинаются с _default,
     если в атрибуте лежит объект `HandlerConfig`, то формируем из него словарь
     конфигурации хэндлера.
    Если для одного из параметров хэндлера не установлено значение (None),
     то проверяем, то пробуем установить значение по умолчанию из атрибута
     `"_default_" + f"attr_name"`.
    Если значения по умолчанию нет, и параметр == None, то этот параметр не
     включается в итоговый конфиг. Если параметр обязателен для loguru,
     оно естественно упадет.
    """

    _default_sink: Any = None
    _default_level: str | int = None
    _default_format: Optional[str | Callable] = None
    _default_filter: Optional[Callable[[dict], bool] | str | dict] = None
    _default_serialize: Optional[bool] = None
    _default_backtrace: Optional[bool] = None
    _default_diagnose: Optional[bool] = None
    _default_colorize: Optional[bool] = None
    _default_enqueue: Optional[bool] = None
    _default_catch: Optional[bool] = None

    def get_handlers_config(self) -> list[dict]:
        handlers = []

        for handler_config in self.handlers_configurations:
            parameters = handler_config.__dict__
            parameters = (
                self._get_parameter_config(key, value)
                for key, value in parameters.items()
            )
            parameters = dict(kv for kv in parameters if kv)

            handlers.append(parameters)

        return handlers

    @property
    def handlers_configurations(self) -> list[HandlerConfig]:
        attrs = [
            attr for attr in dir(self)
            if not attr.startswith("_default_")
               and attr != "handlers_configurations"
        ]
        values = [getattr(self, attr) for attr in attrs]

        return [value for value in values if isinstance(value, HandlerConfig)]

    def _get_parameter_config(self, parameter: str, value: Any) \
            -> Optional[tuple[str, Any]]:
        if value is None:
            try:
                return parameter, getattr(self, f"_default_{parameter}")
            except AttributeError:
                return None

        return parameter, value
