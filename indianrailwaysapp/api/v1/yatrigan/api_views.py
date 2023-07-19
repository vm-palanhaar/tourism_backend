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
        shops = IRModel.Shop.objects.filter(station=kwargs['station'])
        if shops.filter(is_active=True, is_verified=True).count() != 0:
            serializer = self.get_serializer(shops.filter(is_active=True, is_verified=True), many=True)
            response_data['shops'] = serializer.data
            return response_200(response_data)
        elif shops.filter(is_active=False).count() != 0 or shops.filter(is_verified=False).count() != 0:
            return response_400(IrError.irShopListInActiveNotVerified(shops[0].station.name, shops[0].station.code))
        else:
            station = IRModel.RailStation.objects.get(code = kwargs['station'])
            return response_400(IrError.irShopListEmpty(station.name, station.code))
        
    

class ShopInvListApi(generics.ListAPIView):
    serializer_class = IRSerializer.ShopInvList

    def get(self, request, *args, **kwargs):
        try:
            shop = IRModel.Shop.objects.get(station=kwargs['station'],id=kwargs['shopId'], is_active=True, is_verified=True)
        except IRModel.Shop.DoesNotExist:
            station = IRModel.RailStation.objects.get(code = kwargs['station'])
            response_data = {
                "shop" : kwargs['shopId'],
                "station" : kwargs['station'],
                "error" : IrError.irShopListEmpty(station.name, station.code)
            }
            return response_400(response_data)
        
        shop_invs = IRModel.ShopInv.objects.filter(shop=shop, is_stock=True)

        if shop_invs.count() == 0:
            response_data = {
                "shop" : kwargs['shopId'],
                "station" : kwargs['station'],
                "error" : IrError.irShopInvListEmpty()
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
            station = IRModel.RailStation.objects.get(code = kwargs['station'])
            error_map = error_map['message'].format(kwargs['station'])
            response_data = {
                'error' : IrError.irShopListEmpty(station.name, station.code)
            }
            return response_400(response_data)        
        
        serializer = self.get_serializer(shop)
        return response_200(serializer.data)
