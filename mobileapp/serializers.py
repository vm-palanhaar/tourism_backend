from rest_framework import serializers

from mobileapp import models


'''
Common APIs Serializer
1. MobileAppFeedbackSerializer
'''

class MobileAppFeedbackSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    class Meta:
        model = models.MobileAppFeedback
        fields = '__all__'
