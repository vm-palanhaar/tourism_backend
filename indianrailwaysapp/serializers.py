from rest_framework import serializers

from indianrailwaysapp import models

'''
Common APIs Serializer
1. RailwayStationListSerializer
2. RailwayStationSerializer

Yatrigan APIs Serializer

iDukaan APIs Serializer

'''

class RailwayStationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RailwayStation
        fields = ['code','name']


class RailwayStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RailwayStation
        fields = ['code','name']