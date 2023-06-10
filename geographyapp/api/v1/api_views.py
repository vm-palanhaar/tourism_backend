from pathlib import Path
import requests
import environ
import os
import json
import urllib.request

from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response

from geographyapp import serializers
from geographyapp import models

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR,'.env'))

env = environ.Env()


'''
PROD
1. RailwayStationListApi
2. RailwayStationApi
DEV
'''

response_map = {"data":None}
failed_response_map = {'error':None}

reverse_geocoding_params_not_valid = 'Latitude or Longitude is missing!'
reverse_geocoding_bad_request = 'Location service is not responding.'

def error_response(error):
    failed_response_map['error'] = error
    return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)


def revGeocodingStateCountry(lat, lng):
    lat = lat
    lng = lng
    if lat == None or lng == None:
        return error_response(reverse_geocoding_params_not_valid)
    mmi_uri = env("MMI_URI").format(apiKey=env("MMI_API_KEY"), lat=lat, lng=lng)
    response = requests.get(mmi_uri)
    if response.status_code == 200:
        json_data = response.json()
        response_map['data'] = {
            'state' : json_data['results'][0]['state'],
            'country' : json_data['results'][0]['area'],
        }
    return response_map
    


class StateAPIView(generics.ListAPIView):
    serializer_class = serializers.StateSerializer

    def get(self, request, *args, **kwargs):
        response_data = {}
        response_data['countryCode'] = kwargs['cid']
        states = models.State.objects.filter(country = kwargs['cid'])
        if states.count() > 0:
            serializer = self.get_serializer(states, many=True)
            response_data['states'] = serializer.data
            return Response(response_data, status=status.HTTP_200_OK)
        response_data['error'] = {
            'code' : 'geoStatesNotFound',
            'message' : f'States data not available for {kwargs["cid"]}'
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    

class ReverseGeocodeAPIView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        response_data = revGeocodingStateCountry(
            lat = request.GET.get("lat"), 
            lng=request.GET.get("lng")
        )
        if response_data['data'] != None:
            return Response(response_data, status=status.HTTP_200_OK)
        failed_response_map['data'] = reverse_geocoding_bad_request
        return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)
        