from django.db.models import (CASCADE, DO_NOTHING, SET_DEFAULT, SET_NULL,
                              BooleanField, CharField, DateField,
                              DateTimeField, ForeignKey, GenericIPAddressField,
                              IntegerField, ManyToManyField, Model,
                              NullBooleanField, OneToOneField,
                              PositiveIntegerField, TextField, FloatField, ImageField)

from libs.utils.djangomodelutils import OverwriteStorage

class OWMData(Model):
    timestamp = DateTimeField(null=True, default=None)
    city = ForeignKey('OWMCities', null=True, default=None,
                      related_query_name='data2city', related_name='data2city',
                      on_delete=DO_NOTHING)
    temperature = FloatField(null=True, default=None)
    temperature_min = FloatField(null=True, default=None)
    temperature_max = FloatField(null=True, default=None)
    pressure = FloatField(null=True, default=None)
    humidity = FloatField(null=True, default=None)
    weather = ForeignKey('OWMWeather', null=True, default=None,
                         related_query_name='data2weather',
                         related_name='data2weather', on_delete=DO_NOTHING)
    clouds = FloatField(null=True, default=None)
    wind_speed = FloatField(null=True, default=None)
    wind_deg = FloatField(null=True, default=None)
    snow_3h = FloatField(null=True, default=None)
    rain_3h = FloatField(null=True, default=None)

    updated = DateTimeField(null=True, default=None)

    @property
    def get_min_temp(self):
        return int(self.temperature_min - 273)

    @property
    def get_max_temp(self):
        return int(self.temperature_max - 273)

    @property
    def get_temp(self):
        return int(self.temperature - 273)


class OWMCities(Model):
    owm_id = IntegerField(null=False, unique=True)
    name = CharField(null=True, default=None, max_length=128)
    longitude = FloatField(null=True, default=None)
    latitude = FloatField(null=True, default=None)
    country = CharField(null=True, default=None, max_length=2)


def weather_icon_path(instance, filename):
    return 'weather/icons/openweathermap/{filename}.png'.format(filename=filename)


class OWMWeather(Model):
    owm_id = IntegerField(null=False, unique=True)
    name = CharField(null=True, default=None, max_length=64)
    description = CharField(null=True, default=None, max_length=128)
    icon = ImageField(upload_to=weather_icon_path, storage=OverwriteStorage(),  null=True, default=None)



