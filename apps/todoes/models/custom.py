from django.db import models
from django.db.models import QuerySet

from apps.todoes.models.todo import RepeatableTODO, TODO


class TodoQuerySet(QuerySet):
    """
    Notes
    -----
    If received object has repeatabletodo attribute, then return RepeatableTODO instance, else TODO.
    If in filter uses fields from RepeatableTODO then it use that model for filtering instead TODO model.
    """
    __repeatable_task_model_fields = set([field.name for field in RepeatableTODO._meta.fields if field.name != "id"])

    def get(self, *args, **kwargs):
        return self._get_instance(super().get(*args, **kwargs))

    def filter(self, *args, **kwargs):
        self._select_queryset_model(*args, **kwargs)
        return super().filter(*args, **kwargs)

    def exclude(self, *args, **kwargs):
        self._select_queryset_model(*args, **kwargs)
        return super().exclude(*args, **kwargs)

    def __getitem__(self, item):
        return self._get_instance(QuerySet.__getitem__(self, item))

    def _get_instance(self, instance):
        try:
            instance.repeatabletodo
        except RepeatableTODO.DoesNotExist:
            pass
        else:
            instance = RepeatableTODO.objects.get(pk=instance.pk)

        return instance

    def _select_queryset_model(self, *args, **kwargs):
        query_fields = set(f for f in kwargs.keys() if f != "id")

        if query_fields.intersection(self.__repeatable_task_model_fields):
            self.model = RepeatableTODO
        else:
            self.model = TODO


class GenericTodoManager(models.Manager):
    def get_queryset(self):
        return TodoQuerySet(self.model, self._db)


class TodoProxy(TODO):
    objects = GenericTodoManager()

    class Meta:
        proxy = True
