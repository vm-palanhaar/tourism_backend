from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from mobileapp import models
from mobileapp import serializers

'''
PROD
1. ProductDetailsApi
DEV
'''

failed_response_map = {'error':None}
response_map = {'data':None}


class MobileAppFeedbackAPIView(generics.CreateAPIView):
    serializer_class = serializers.MobileAppFeedbackSerializer

    def post(self, request, *args, **kwargs):       
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        failed_response_map['error'] = 'Something went wrong!'
        return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
