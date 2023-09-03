from rest_framework import generics, status
from rest_framework.response import Response

from indianrailwaysapp import serializers as IRSerializer
from indianrailwaysapp import models as IRModel


class RailStationListApi(generics.GenericAPIView):
    serializer_class = IRSerializer.RailStationList

    def get(self, request, *args, **kwargs):
        stations = IRModel.RailStation.objects.all()
        serializer = self.get_serializer(stations, many=True)
        stations = []
        for station in serializer.data:
            stations.append(station['station'])
        response_data = {
            "total" : len(stations),
            "stations" : stations,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    

class IrHelplineListApi(generics.ListAPIView):
    serializer_class = IRSerializer.IrHelplineNumberList

    def get(self, request, *args, **kwargs):
        numbers = IRModel.IrHelplineNumber.objects.filter(state__isnull=True)
        serializer = self.get_serializer(numbers, many=True)
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)

    
class IrGRPListApi(generics.ListAPIView):
    serializer_class = IRSerializer.IrGRPList

    def get(self, request, *args, **kwargs):
        numbers = IRModel.IrHelplineNumber.objects.filter(state__isnull=False)
        serializer = self.get_serializer(numbers, many=True)
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)
    

