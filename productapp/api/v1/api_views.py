from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from productapp import models as PCModel
from productapp import serializers as PCSerializer

'''
PROD
1. ProductDetailsApi
DEV
'''

failed_response_map = {'error':None}
response_map = {'data':None}

product_not_found = 'Product not found!'

class ProductAPIView(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        try:
            product = PCModel.Product.objects.get(id=kwargs['productid'])
        except PCModel.Product.DoesNotExist:
            failed_response_map['error'] = product_not_found
            return Response(failed_response_map, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PCSerializer.ProductSerializer(product)
        response_map['data'] = serializer.data
        return Response(response_map, status=status.HTTP_200_OK)
