from rest_framework import serializers

from geographyapp import models


class StateSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = models.State
        fields = ['id','name']
