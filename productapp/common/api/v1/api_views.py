from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from productapp import models as PCModel
from productapp import serializers as PCSerializer
from productapp.common.api import errors as PcError

'''
PROD
1. ProdInfoApi
DEV
'''

def response_200(response_fail):
    return Response(response_fail, status=status.HTTP_200_OK)

def response_400(response_fail):
    return Response(response_fail, status=status.HTTP_400_BAD_REQUEST)


class ProdInfoApi(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        response_data = {}
        response_data['id'] = kwargs['productId']
        try:
            product = PCModel.Prod.objects.get(id=kwargs['productId'])
        except PCModel.Prod.DoesNotExist:
            response_data.update(PcError.pcProdNotFound())
            return response_400(response_data)
        
        serializer = PCSerializer.ProductSerializer(product)
        response_data = serializer.data
        return response_200(response_data)
