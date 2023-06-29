from rest_framework import generics, status
from rest_framework.response import Response

from indianrailwaysapp import serializers as IRSerializer
from indianrailwaysapp import models as IRModel
from indianrailwaysapp.api.v1.yatrigan import errors as IrError
from apiutil import errors as UtilError



'''
PROD APIs
1. TrainListApi
2. TrainScheduleApi
3. ShopListApi
4. ShopInvListApi
5. ShopInfoApi

DEV APIs

'''


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

def response_200(response_data):
    return Response(response_data, status=status.HTTP_200_OK)

def response_400(response_data):
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)



class TrainListApi(generics.ListAPIView):
    serializer_class = IRSerializer.TrainList_Yatrigan

    def get(self, request, *args, **kwargs):
        trains = IRModel.Train.objects.all()
        serializer = self.get_serializer(trains, many=True)
        trains = []
        for station in serializer.data:
            trains.append(station['train'])
        response_data = {
            "total" : len(trains),
            "trains" : trains,
        }
        return response_200(response_data)


class TrainScheduleApi(generics.GenericAPIView):
    serializer_class = IRSerializer.TrainSchedule_Yatrigan

    def get(self, request, *args, **kwargs):
        if request.headers['train'] == None:
            return response_400(UtilError.error_bad_action_anon)
        try:
            train = IRModel.Train.objects.get(train_no=request.headers['train'])
        except IRModel.Train.DoesNotExist:
            return response_400(IrError.train_not_found)
        serializers = self.get_serializer(train)
        return response_200(serializers.data)


class ShopListApi(generics.ListAPIView):
    serializer_class = IRSerializer.ShopList_Yatrigan

    def get(self, request, *args, **kwargs):
        response_data = {}
        response_data['station'] = kwargs['station']
        shops = IRModel.Shop.objects.filter(station=kwargs['station'], is_active=True, is_open=True)
        if shops.count() == 0:
            error_map = IrError.shop_not_found
            error_map['message'] = error_map['message'].format(kwargs['station'])
            response_data['error'] = IrError.shop_not_found
            return response_400(response_data)
        serializer = self.get_serializer(shops, many=True)
        response_data['shops'] = serializer.data
        return response_200(response_data)
    

class ShopInvListApi(generics.ListAPIView):
    serializer_class = IRSerializer.ShopInvList

    def get(self, request, *args, **kwargs):
        shop = IRModel.Shop.objects.filter(station=kwargs['station'], id=kwargs['shopId'], is_active=True, is_open=True)
        if shop.count() == 0:
            error_map = IrError.shop_not_found
            error_map = error_map['message'].format(kwargs['station'])
            response_data = {
                "shop" : kwargs['shopId'],
                "station" : kwargs['station'],
                "error" : error_map
            }
            return response_400(response_data)
        
        shop_invs = IRModel.ShopInv.objects.filter(shop=kwargs['shopId'], is_stock=True)
        if shop_invs.count() == 0:
            response_data = {
                "shop" : kwargs['shopId'],
                "station" : kwargs['station'],
                "error" : IrError.shops_inv_list_not_found
            }
            return response_400(response_data)
        
        serializer = self.get_serializer(shop_invs, many=True)
        response_data = {
            "shop" : kwargs['shopId'],
            "station" : kwargs['station'],
            "inv" : serializer.data 
        }
        return response_200(response_data)


class ShopInfoApi(generics.RetrieveAPIView):
    serializer_class = IRSerializer.ShopInfo_Yatrigan

    def get(self, request, *args, **kwargs):
        try:
          shop = IRModel.Shop.objects.get(station=kwargs['station'], id=kwargs['shopId'], is_active=True, is_open=True)
        except IRModel.Shop.DoesNotExist:
            error_map = IrError.shop_not_found
            error_map = error_map['message'].format(kwargs['station'])
            response_data = {
                'error' : error_map
            }
            return response_400(response_data)
        
        serializer = self.get_serializer(shop)
        return response_200(serializer.data)
