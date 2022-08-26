from loguru import logger

from django.db import models

from libs.utils.djangomodelutils import OverwriteStorage


__all__ = ["OWMData", "OWMCities", "OWMWeather"]


class OWMData(models.Model):
    timestamp = models.DateTimeField(null=True, default=None)
    city = models.ForeignKey(
        "OWMCities",
        null=True, default=None,
        related_query_name="data2city",
        related_name="data2city",
        on_delete=models.DO_NOTHING
    )
    temperature = models.FloatField(null=True, default=None)
    temperature_min = models.FloatField(null=True, default=None)
    temperature_max = models.FloatField(null=True, default=None)
    pressure = models.FloatField(null=True, default=None)
    humidity = models.FloatField(null=True, default=None)
    weather = models.ForeignKey(
        "OWMWeather",
        null=True, default=None,
        related_query_name="data2weather", 
        related_name="data2weather",
        on_delete=models.DO_NOTHING
    )
    clouds = models.FloatField(null=True, default=None)
    wind_speed = models.FloatField(null=True, default=None)
    wind_deg = models.FloatField(null=True, default=None)
    snow_3h = models.FloatField(null=True, default=None)
    rain_3h = models.FloatField(null=True, default=None)

    # TODO: should be `auto_now`
    updated = models.DateTimeField(null=True, default=None)

    @property
    def get_min_temp(self):
        return int(self.temperature_min - 273)

    @property
    def get_max_temp(self):
        return int(self.temperature_max - 273)

    @property
    def get_temp(self):
        return int(self.temperature - 273)


class OWMCities(models.Model):
    owm_id = models.IntegerField(null=False, unique=True)
    name = models.CharField(null=True, default=None, max_length=128)
    longitude = models.FloatField(null=True, default=None)
    latitude = models.FloatField(null=True, default=None)
    country = models.CharField(null=True, default=None, max_length=2)

    @classmethod
    def update_city_data(cls, city_data):
        logger.debug(f"Start creating city data in db with input <{city_data}>.")
        instance, _ = cls.objects.get_or_create(owm_id=city_data['id'])

        logger.debug(
            f"City with owm_id <{instance.owm_id}> " +
            ("was created." if _ else "was found in db.")
        )

        instance.name = city_data['name']
        instance.country = city_data['country']
        instance.latitude = city_data['coord']['lat']
        instance.longitude = city_data['coord']['lon']

        instance.save()

        logger.debug("New city data saved in db.")

        return instance


def weather_icon_path(instance, filename):
    return f"weather/icons/openweathermap/{filename}.png"


class OWMWeather(models.Model):
    owm_id = models.IntegerField(null=False, unique=True)
    name = models.CharField(null=True, default=None, max_length=64)
    description = models.CharField(null=True, default=None, max_length=128)
    icon = models.ImageField(
        upload_to=weather_icon_path,
        storage=OverwriteStorage(),
        null=True,
        default=None
    )



