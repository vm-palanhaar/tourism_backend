from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from indianrailwaysapp import serializers as IRSerializer
from indianrailwaysapp import models as IRModel


failed_response_map = {'error':None}
response_map = {'data':None}

is_error = 'Something went wrong. Issue reported to Team and your account will be de-activated.'

train_not_found = 'Train not available!'
shops_list_not_found_1 = 'Stalls are not present on this station!'
shops_list_not_found_2 = 'Pending verification for stalls!'
shops_list_not_found_3 = 'Stalls are not registered on iDukaan!'
shops_inv_list_not_found_1 = 'Products are not listed/available on this stall!'



def error_response(error):
    failed_response_map['error'] = error
    return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)

def error_response_400(failed_response_map):
    return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)



class TrainListAPIView(generics.ListAPIView):
    serializer_class = IRSerializer.TrainListSerializer

    def get(self, request, *args, **kwargs):
        trains = IRModel.Train.objects.all()
        serializer = self.get_serializer(trains, many=True)
        trains = []
        for station in serializer.data:
            trains.append(station['train'])
        response_map["data"] = {
            "total" : len(trains),
            "trains" : trains,
        }
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


class ShopListAPIView(generics.ListAPIView):
    serializer_class = IRSerializer.ShopListSerializer_Yatrigan

    def get(self, request, *args, **kwargs):
        shops = IRModel.Shop.objects.filter(station=kwargs['station'], is_active=True, is_open=True)
        if shops.count() == 0:
          failed_response_map = {
            "station" : kwargs['station'],
            "error" : [
                shops_list_not_found_1,
                shops_list_not_found_2,
                shops_list_not_found_3
                ]
          }
          return error_response_400(failed_response_map)
        serializer = self.get_serializer(shops, many=True)
        response_map = {
            "station" : kwargs['station'],
            "shops" : serializer.data 
        }
        return Response(response_map, status=status.HTTP_200_OK)
    

class ShopInventoryListAPIView(generics.ListAPIView):
    serializer_class = IRSerializer.ShopInventoryListSerializer

    def get(self, request, *args, **kwargs):
        shop = IRModel.Shop.objects.filter(station=kwargs['station'], id=kwargs['shopId'], is_active=True, is_open=True)
        if shop.count() == 0:
          failed_response_map = {
            "shop" : kwargs['shopId'],
            "station" : kwargs['station'],
            "error" : [
                shops_list_not_found_1,
                shops_list_not_found_2,
                shops_list_not_found_3
                ]
          }
          return error_response_400(failed_response_map)
        
        shop_invs = IRModel.ShopInventory.objects.filter(shop=kwargs['shopId'], is_stock=True)
        if shop_invs.count() == 0:
            failed_response_map = {
                "shop" : kwargs['shopId'],
                "station" : kwargs['station'],
                "error" : shops_inv_list_not_found_1
            }
            return error_response_400(failed_response_map)
        serializer = self.get_serializer(shop_invs, many=True)
        response_map = {
            "shop" : kwargs['shopId'],
            "station" : kwargs['station'],
            "inv" : serializer.data 
        }
        return Response(response_map, status=status.HTTP_200_OK)


class ShopDetailsAPIView(generics.RetrieveAPIView):
    serializer_class = IRSerializer.ShopDetailsSerializer_Yatrigan

    def get(self, request, *args, **kwargs):
        try:
          shop = IRModel.Shop.objects.get(station=kwargs['station'], id=kwargs['shopId'], is_active=True, is_open=True)
        except IRModel.Shop.DoesNotExist:
          return error_response([shops_list_not_found_1,shops_list_not_found_2,shops_list_not_found_3])  
        serializer = self.get_serializer(shop)
        response_map['data'] = serializer.data
        return Response(response_map, status=status.HTTP_200_OK)

    
