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

is_error = 'Something went wrong. Issue reported to Team and your account will be de-activated.'

train_not_found = 'Train not available!'

def error_response(error):
    failed_response_map['error'] = error
    return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)


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
    

class TrainListAPIView(generics.ListAPIView):
    serializer_class = IRSerializer.TrainListSerializer

    def get(self, request, *args, **kwargs):
        trains = IRModel.Train.objects.all()
        serializer = self.get_serializer(trains, many=True)
        response_map['data'] = serializer.data
        return Response(response_map)
    

class TrainScheduleAPIView(generics.GenericAPIView):
    serializer_class = IRSerializer.TrainScheduleSerializer

    def get(self, request, *args, **kwargs):
        if request.headers['train'] == None:
            return error_response(is_error)
        
        try:
            train = IRModel.Train.objects.get(train_no=request.headers['train'])
        except IRModel.Train.DoesNotExist:
            return error_response(train_not_found)
        
        serializers = self.get_serializer(train)
        response_map['data'] = serializers.data
        return Response(response_map)


class TrainStationListAPIView(generics.ListAPIView):
    serializer_class = IRSerializer.TrainStationListSerializer

    def get(self, request, *args, **kwargs):
        if request.headers['train'] == None:
            return error_response(is_error)
        
        try:
            train = IRModel.Train.objects.get(train_no=request.headers['train'])
        except IRModel.Train.DoesNotExist:
            return error_response(train_not_found)
        
        serializer = self.get_serializer(train)
        response_map['data'] = serializer.data
        return Response(response_map)


