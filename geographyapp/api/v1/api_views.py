from rest_framework import generics, status
from rest_framework.response import Response

from geographyapp import serializers
from geographyapp import models


'''
PROD
1. RailwayStationListApi
2. RailwayStationApi
DEV
'''

response_map = {"data":None}
failed_response_map = {'error':None}

def error_response(error):
    failed_response_map['error'] = error
    return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)


class StateAPIView(generics.ListAPIView):
    serializer_class = serializers.StateSerializer

    def get(self, request, *args, **kwargs):
        states = models.State.objects.filter(country = kwargs['cid'])
        if states.count() > 0:
            serializer = self.get_serializer(states, many=True)
            response_map['data'] = serializer.data
            return Response(response_map, status=status.HTTP_200_OK)
        
        return error_response(f'States data not available for {kwargs["cid"]}')
        