from rest_framework import generics, status
from rest_framework.response import Response

from indianrailwaysapp import serializers as IRSerializer
from indianrailwaysapp import models as IRModel

from geographyapp.api.v1 import api_views as GeoV1

'''
PROD
1. RailwayStationListApi
2. RailwayStationApi
DEV
'''

response_map = {"data":None}
failed_response_map = {'error':None}


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
    


class IrGRPStateAPIView(generics.ListAPIView):
    serializer_class = IRSerializer.IrGRPListSerializer

    def get(self, request, *args, **kwargs):
        if request.GET.get('lat') == None or request.GET.get('lng') == None:
            return GeoV1.error_response(GeoV1.reverse_geocoding_params_not_valid)
        response_data =  GeoV1.revGeocodingStateCountry(
            lat = request.GET.get("lat"), 
            lng=request.GET.get("lng")
            )
        if response_data['data'] != None:
            numbers = IRModel.IrGRP.objects.get(state__name=response_data['data']['state'])
            serializer = self.get_serializer(numbers)
            response_map["data"] = serializer.data
            return Response(response_map, status=status.HTTP_200_OK)
        failed_response_map['data'] = GeoV1.reverse_geocoding_bad_request
        return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
