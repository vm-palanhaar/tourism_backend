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
    serializer_class = IRSerializer.RailwayStationListSerializer

    def get(self, request, *args, **kwargs):
        stations = IRModel.RailwayStation.objects.all()
        serializer = self.get_serializer(stations, many=True)
        response_map["data"] = serializer.data
        return Response(response_map, status=status.HTTP_200_OK)
    

class IrGRPListAPIView(generics.ListAPIView):
    serializer_class = IRSerializer.IrGRPListSerializer

    def get(self, request, *args, **kwargs):
        numbers = IRModel.IrGRP.objects.all()
        serializer = self.get_serializer(numbers, many=True)
        response_map["data"] = serializer.data
        return Response(response_map, status=status.HTTP_200_OK)
