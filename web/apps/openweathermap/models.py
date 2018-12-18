from django.db.models import (CASCADE, DO_NOTHING, SET_DEFAULT, SET_NULL,
                              BooleanField, CharField, DateField,
                              DateTimeField, ForeignKey, GenericIPAddressField,
                              IntegerField, ManyToManyField, Model,
                              NullBooleanField, OneToOneField,
                              PositiveIntegerField, TextField, FloatField)

class OWMData(Model):
    timestamp = DateTimeField(null=True, default=None)
    city = ForeignKey('OWMCities', null=True, default=None,
                      related_query_name='data2city', related_name='data2city',
                      on_delete=DO_NOTHING)
    temperature = FloatField()
    temperature_min = FloatField()
    temperature_max = FloatField()
    pressure = FloatField()
    humidity = FloatField()
    weather = ForeignKey('OWMWeather', null=True, default=None,
                         related_query_name='data2weather',
                         related_name='data2weather', on_delete=DO_NOTHING)
    clouds = FloatField()
    wind_speed = FloatField()
    wind_deg = FloatField()
    snow_3h = FloatField()
    rain_3h = FloatField()

    updated = DateTimeField(null=True, default=None)


class OWMCities(Model):
    owm_id = IntegerField(null=False, unique=True)
    name = CharField(null=True, default=None, max_length=128)
    longitude = FloatField(null=True, default=None)
    latitude = FloatField(null=True, default=None)
    country = CharField(null=True, default=None, max_length=2)


class OWMWeather(Model):
    owm_id = IntegerField(null=False, unique=True)
    name = CharField(null=True, default=None, max_length=64)
    description = CharField(null=True, default=None, max_length=128)
    icon = CharField(null=True, default=None, max_length=16) #TODO переделать в FileField()