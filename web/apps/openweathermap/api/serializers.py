from rest_framework import serializers

from web.apps.openweathermap.models import OWMWeather, OWMData

__all__ = ['OWMWeatherSerializer', 'OWMDataSerializer']


class OWMWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = OWMWeather
        fields = ['owm_id', 'name', 'description', 'icon']


class OWMDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OWMData
        fields = ['timestamp', 'temperature', 'pressure', 'humidity', 'weather']
