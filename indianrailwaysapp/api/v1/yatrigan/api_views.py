from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from indianrailwaysapp import serializers as ShopSerializer
from indianrailwaysapp import models as ShopModel
from businessapp import models as OrgModel
from userapp import models as UserModel
from productapp import models as PcModel
from productapp import serializers as PcSerializer


failed_response_map = {'error':None}
response_map = {'data':None}

shops_list_not_found_1 = 'Stalls are not present on this station!'
shops_list_not_found_2 = 'Pending verification for stalls!'
shops_list_not_found_3 = 'Stalls are not registered on iDukaan!'
shops_inv_list_not_found_1 = 'No products are available on this stall!'
shops_inv_list_not_found_2 = 'Pending verification for products!'



def error_response(error):
    failed_response_map['error'] = error
    return Response(failed_response_map, status=status.HTTP_400_BAD_REQUEST)

class ShopListAPIView(generics.ListAPIView):
    serializer_class = ShopSerializer.ShopListSerializer_Yatrigan

    def get(self, request, *args, **kwargs):
        shops = ShopModel.Shop.objects.filter(station=kwargs['station'], is_active=True, is_open=True)
        if shops.count() == 0:
          return error_response([shops_list_not_found_1,shops_list_not_found_2,shops_list_not_found_3])  
        serializer = self.get_serializer(shops, many=True)
        response_map['data'] = serializer.data
        return Response(response_map, status=status.HTTP_200_OK)
    

class ShopInventoryListAPIView(generics.ListAPIView):
    serializer_class = ShopSerializer.ShopInventoryListSerializer

    def get(self, request, *args, **kwargs):
        shop = ShopModel.Shop.objects.filter(station=kwargs['station'], id=kwargs['shopId'], is_active=True, is_open=True)
        if shop.count() == 0:
          return error_response([shops_list_not_found_1,shops_list_not_found_2,shops_list_not_found_3])  
        
        shop_invs = ShopModel.ShopInventory.objects.filter(shop=kwargs['shopId'], is_stock=True)
        if shop_invs.count() == 0:
            return error_response([shops_inv_list_not_found_1,shops_inv_list_not_found_2])
        serializer = self.get_serializer(shop_invs, many=True)
        response_map['data'] = serializer.data
        return Response(response_map, status=status.HTTP_200_OK)


class ShopDetailsAPIView(generics.RetrieveAPIView):
    serializer_class = ShopSerializer.ShopDetailsSerializer_Yatrigan

    def get(self, request, *args, **kwargs):
        try:
          shop = ShopModel.Shop.objects.get(station=kwargs['station'], id=kwargs['shopId'], is_active=True, is_open=True)
        except ShopModel.Shop.DoesNotExist:
          return error_response([shops_list_not_found_1,shops_list_not_found_2,shops_list_not_found_3])  
        serializer = self.get_serializer(shop)
        response_map['data'] = serializer.data
        return Response(response_map, status=status.HTTP_200_OK)

    
