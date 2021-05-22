from rest_framework import serializers

from apps.openweathermap.models import OWMWeather, OWMData

__all__ = ['OWMWeatherSerializer', 'OWMDataSerializer']


class OWMWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = OWMWeather
        fields = ["id", 'owm_id', 'name', 'description', 'icon']


class OWMDataSerializer(serializers.ModelSerializer):
    weather_data = OWMWeatherSerializer(source='weather')

    class Meta:
        model = OWMData
        fields = [
            "id", 'timestamp', 'temperature', 'pressure', 'humidity',
            'weather', 'weather_data'
        ]
