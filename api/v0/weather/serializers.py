from rest_framework import serializers

from apps.openweathermap.models import OWMWeather, OWMData

__all__ = ['OWMWeatherSerializer', 'OWMDataSerializer']


class OWMWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = OWMWeather
        fields = ['owm_id', 'name', 'description', 'icon']


class OWMDataSerializer(serializers.HyperlinkedModelSerializer):
    # TODO temporally while spa in development. Must be remove in future,
    #  because spa must make api_request for get image.
    weather_data = OWMWeatherSerializer(source='weather')

    class Meta:
        model = OWMData
        fields = ['timestamp', 'temperature', 'pressure', 'humidity', 'weather', 'weather_data']
