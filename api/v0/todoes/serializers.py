from rest_framework import serializers

from apps.todoes.models import TODO, RepeatableTODO, RepeatableTODOHistory

__all__ = ["TODOSerializer", ]


class RepeatableTODOSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RepeatableTODO
        fields = ["repeat_every_minutes", "start_at"]


class TODOSerializer(serializers.HyperlinkedModelSerializer):
    repeat_every = serializers.IntegerField(source="repeatabletodo.repeat_every_minutes", required=False)
    start_at = serializers.DateTimeField(source="repeatabletodo.start_at", read_only=True)

    class Meta:
        model = TODO
        fields = [
            "id", "title", "description", "created", "updated",
            "repeat_every", "start_at",
        ]

    def create(self, validated_data):
        print(validated_data)

        try:
            repeatable = validated_data.pop("repeatabletodo")
        except KeyError:
            repeatable = {}

        validated_data = {**validated_data, **repeatable}

        ModelClass = RepeatableTODO if repeatable else TODO

        todo = ModelClass.objects.create(**validated_data)

        return todo
