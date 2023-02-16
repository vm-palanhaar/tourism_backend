from rest_framework import generics
from rest_framework import generics, status
from rest_framework.response import Response

from indianrailwaysapp import serializers as IRSerializer
from indianrailwaysapp import models as IRModel

'''
PROD
1. RailwayStationListApi
2. RailwayStationApi
DEV
'''

response_map = {"data":None}


class RailwayStationListAPIView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        stations = IRModel.RailwayStation.objects.all()
        serializer = IRSerializer.RailwayStationListSerializer(stations, many=True)
        response_map["data"] = serializer.data
        return Response(response_map, status=status.HTTP_200_OK)