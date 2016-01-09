from rest_framework import serializers

from station.models import Station
from station.models import Box
from station.models import Stand
from station.models import Service
from station.models import Job


class StationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station


class BoxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Box


class StandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stand


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'date_time', 'stand')
